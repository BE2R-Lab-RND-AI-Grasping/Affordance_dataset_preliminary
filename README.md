Download the [dataset](https://disk.yandex.ru/d/wn96YnqAKPJ_Zw) and extract to the project directory

The dataset includes several tools from the HANDAL dataset. For each tool there are several instances and for each instance the dataset contains:
- initial 3d model in .ply format
- handle 3d model in .ply format
- object convex decomposition in the form of the .obj files of the parts and the 3d model merged from the convex parts
- the point cloud sampled from the merged model
- the color labeled point cloud with red points representing the handle and the gray points representing non-handle part of the tool  


The extracted dataset should have the paths
```bash
    |-- dataset
        |-- combinational_wrenches
            |-- model_0
                |-- handle.ply
                |-- initial_object.ply
                |-- object_convex_decomposition.obj
                |-- object_part_0.obj # usually several part files
                |-- point_cloud_colorless.ply
                |-- point_cloud_labeled.ply
        |-- fixed_joint_pliers
```

To set up the environment with `conda` use:
```bash
    conda env create -f environment.yml
    conda activate dataset
```
For visualization use vis.ipynb and set the path to the model of interest in the second code cell with:
```bash
    model_dir = Path("./dataset/path/to/model")
```





