# ComfyUI Conditioning Saver

Save and load CONDITIONING variables to/from files, enabling reuse of encoded prompts across workflows.

## Nodes

### SaveConditioning
Saves any CONDITIONING input to a `.cond` file in the `output/conditioning/` directory.

**Inputs:**
- `conditioning` — The CONDITIONING to save
- `filename_prefix` — Output filename prefix (default: `conditioning/ComfyUI`)

### LoadConditioning
Loads a `.cond` file from the `input/conditioning/` directory.

**Inputs:**
- `conditioning_file` — Select from available `.cond` files

**Outputs:**
- `CONDITIONING` — The loaded conditioning

## Usage

1. Add **SaveConditioning** to your workflow, connect any CONDITIONING output
2. Run the workflow — the `.cond` file is saved to `output/conditioning/`
3. Move the `.cond` file to `input/conditioning/`
4. Use **LoadConditioning** in any workflow to reload it

This is useful for caching expensive CLIP encodings or sharing conditioning between workflows without re-encoding.
