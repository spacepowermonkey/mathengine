# mathengine
This repo is an ALPHA implementation of a mathematical reasoning engine built atop projecting categorical semantics as digital images.



## Usage
MathEngine requires a system with Docker, as it uses containers to standardize the runtime.

`make clean` : this command will erase any existing Docker resources. WARNING: not currently appropriately scoped.

`make docker-mathengine` : this command will build the MathEngine container, including demos and papers.

`make demo-5cubes` : this command will execute the demo and extract the images to the `render/` folder.

`make paper_shapes_as_di` : this command will execute the paper definition and extract the images to the `render/` folder.



## Repo Outline
The repo has three components to it:
- the `src/` folder which contains the MathEngine library;
- the `demo/` folder which contains a few demos of using MathEngine; and,
- the `papers` folder which contains strucutres used in ZMGS Abstract papers.

There are additional supporting files, such as a `Dockerfile` for the MathEngine and a `Makefile` for builds, demos, and papers. The `render/` folder is used by some commands to save data.
