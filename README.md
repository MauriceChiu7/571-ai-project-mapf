### Before training PRIMAL model:
- cd into the `od_mstar3` folder.
- python3 setup.py build_ext (may need --inplace as extra argument).
- copy so object from build/lib.*/ at the root of the od_mstar3 folder.
- Check by going back to the root of the git folder, running python3 and `import cpp_mstar`

Download the `saved_environments` [here](https://drive.google.com/file/d/193mv6mhlcu9Bqxs6hSMTfSk_1GrPAiNO/view?usp=sharing)) and put under PRIMAL folder.
Download the pretrained model [here](https://drive.google.com/file/d/1AtAeUwLF1Rn_X3b2FHkHi4fI5vveUHF6/view?usp=sharing) and put under PRIMAL folder.

To train PRIMAL, run `python primal_train.py` or submit batch job on Purdue scholar cluster with `sbatch strain.sh`

To run the demo video for CBS:
 - Uncomment line 327 of turtlebot3.py then run `python turtlebot3.py --alg cbs`

To run the demo video for PRIMAL:
- Put the pretrained model inside `PRIMAL/model_primal`
- Uncomment line 328 of `turtlebot3.py` then run `python turtlebot3.py --alg primal --offline`