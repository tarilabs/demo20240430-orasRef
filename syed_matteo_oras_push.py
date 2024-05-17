# from Syed

import os
import sys

import oras.defaults
import oras.oci
import oras.provider
from oras.decorator import ensure_container
import logging
from pprint import pprint
from datetime import datetime
import oras.utils


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class Registry(oras.provider.Registry):
    def __init__(self):
        oras.provider.Registry.__init__(self, insecure=True)

    @ensure_container
    def push(self, container, archives: list):
        """
        Given a list of layer metadata (paths and corresponding mediaType) push.
        """
        # Prepare a new manifest
        manifest = oras.oci.NewManifest()

        # Upload files as blobs
        for item in archives:
            logger.info(f"parsing {item} for blob upload")
            blob = item.get("path")
            media_type = (
                item.get("media_type") or "application/vnd.org.dinosaur.tool.datatype.v1+json"
            )
            annots = item.get("annotations") or {}

            if not blob or not os.path.exists(blob):
                logger.warning(f"Path {blob} does not exist or is not defined.")
                continue

            # Artifact title is basename or user defined
            blob_name = item.get("title") or os.path.basename(blob)

            # If it's a directory, we need to compress
            cleanup_blob = False
            if os.path.isdir(blob):
                blob = oras.utils.make_targz(blob)
                cleanup_blob = True

            # Create a new layer from the blob
            layer = oras.oci.NewLayer(blob, media_type, is_dir=cleanup_blob)
            logger.debug(f"Preparing layer {layer}")

            # Update annotations with title we will need for extraction
            annots.update({oras.defaults.annotation_title: blob_name})
            layer["annotations"] = annots

            # update the manifest with the new layer
            manifest["layers"].append(layer)

            # Upload the blob layer
            logger.info(f"Uploading {blob} to {container.uri}")
            response = self.upload_blob(blob, container, layer)
            self._check_200_response(response)

            # Do we need to cleanup a temporary targz?
            if cleanup_blob and os.path.exists(blob):
                os.remove(blob)

        # Prepare manifest and config (add your custom annotations here)
        manifest["annotations"] = {}
        conf, config_file = oras.oci.ManifestConfig()
        conf["annotations"] = {}

        # Config is just another layer blob!
        logger.debug(f"Preparing config {conf}")
        with (
            oras.provider.temporary_empty_config()
        ) as config_file:
            layer = oras.oci.NewLayer(config_file, media_type, is_dir=False)
            response = self.upload_blob(
                config_file, container, layer
            )
            self._check_200_response(response)

        # # Final upload of the manifest
        manifest["config"] = conf
        pprint(manifest)
        self._check_200_response(self.upload_manifest(manifest, container))
        print(f"Successfully pushed {container}")
        return response


def get_oras_client():
    """
    Consistent method to get an oras client
    """
    user = os.environ.get("ORAS_USER")
    password = os.environ.get("ORAS_PASS")
    reg = Registry()
    if user and password:
        print("Found username and password for basic auth")
        reg.set_basic_auth(user, password)
    else:
        logger.warning("No ORAS_USER or ORAS_PASS defined, no auth.")
    return reg



def push(uri, root):
    """
    Given an ORAS identifier, save artifacts to it.
    """
    oras_cli = get_oras_client()

    # Create lookup of archives - relative path and mediatype
    archives = []
    now = datetime.now()

    # Using os.listdir assumes we have single files at the base of our root.
    for filename in os.listdir(root):
        logger.info(f"got {filename}.")
        # use some logic here to derive the mediaType
        media_type = "application/vnd.org.dinosaur.tool.datatype.v1+json"

        # Add some custom annotations!
        size = os.path.getsize(os.path.join(root, filename))  # bytes
        annotations = {"creationTime": str(now), "size": str(size)}
        archives.append(
            {
                "path": filename,
                "title": filename,
                "media_type": media_type,
                "annotations": annotations,
             }
         )

    # Push should be relative to cache context
    with oras.utils.workdir(root):
        oras_cli.push(uri, archives)


push("localhost:8080/dinosaur/artifact:v1", os.getcwd()+"/models")

