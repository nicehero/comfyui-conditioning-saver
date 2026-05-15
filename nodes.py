import os
import hashlib
import json

import torch
import folder_paths

from comfy.comfy_types import IO, FileLocator


class SaveConditioning:
    SEARCH_ALIASES = ["save conditioning", "export conditioning"]

    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "conditioning": (IO.CONDITIONING,),
                "filename_prefix": ("STRING", {"default": "conditioning/ComfyUI"}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = ()
    FUNCTION = "save"
    OUTPUT_NODE = True
    CATEGORY = "conditioning"

    def save(self, conditioning, filename_prefix="ComfyUI", prompt=None, extra_pnginfo=None):
        full_output_folder, filename, counter, subfolder, filename_prefix = (
            folder_paths.get_save_image_path(filename_prefix, self.output_dir)
        )

        results: list[FileLocator] = []
        file = f"{filename}_{counter:05}_.cond"
        results.append({
            "filename": file,
            "subfolder": subfolder,
            "type": "output",
        })

        filepath = os.path.join(full_output_folder, file)
        torch.save(conditioning, filepath)
        return {"ui": {"conditioning": results}}


class LoadConditioning:
    SEARCH_ALIASES = ["load conditioning", "import conditioning", "open conditioning"]

    @classmethod
    def input_dir(cls):
        d = os.path.join(folder_paths.get_input_directory(), "conditioning")
        os.makedirs(d, exist_ok=True)
        return d

    @classmethod
    def INPUT_TYPES(cls):
        d = cls.input_dir()
        files = [
            f for f in os.listdir(d)
            if os.path.isfile(os.path.join(d, f)) and f.endswith(".cond")
        ]
        return {"required": {"conditioning_file": [sorted(files)]}}

    RETURN_TYPES = (IO.CONDITIONING,)
    FUNCTION = "load"
    CATEGORY = "conditioning"

    @classmethod
    def _filepath(cls, conditioning_file):
        return os.path.join(cls.input_dir(), os.path.basename(conditioning_file))

    def load(self, conditioning_file):
        filepath = self._filepath(conditioning_file)
        conditioning = torch.load(filepath, map_location="cpu", weights_only=False)
        return (conditioning,)

    @classmethod
    def IS_CHANGED(cls, conditioning_file):
        filepath = cls._filepath(conditioning_file)
        m = hashlib.sha256()
        with open(filepath, "rb") as f:
            m.update(f.read())
        return m.digest().hex()

    @classmethod
    def VALIDATE_INPUTS(cls, conditioning_file):
        filepath = cls._filepath(conditioning_file)
        if not os.path.exists(filepath):
            return f"Invalid conditioning file: {conditioning_file}"
        return True


NODE_CLASS_MAPPINGS = {
    "SaveConditioning": SaveConditioning,
    "LoadConditioning": LoadConditioning,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveConditioning": "Save Conditioning",
    "LoadConditioning": "Load Conditioning",
}
