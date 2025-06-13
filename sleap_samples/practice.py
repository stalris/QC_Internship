import numpy
import h5py

def list_group_info(:


try:
     with h5py.File("predictions.analysis.h5", "r") as f:
         print("worked!")
         print(f"root: {f.name}")
         print(f"keys: {list(f.keys())}")
         print(f"node_names: {f['node_names'].name}")

     
         
except Exception as e:
    print(f"Error: new to error handling in python.\nCatching all exceptions here.\nException: {e}")
