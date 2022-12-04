# Before training PRIMAL model:
1. Requires python version 3.6
2. `pip install -r requirements.txt`
3. cd into the `od_mstar3` folder.
4. `python3 setup.py build_ext --inplace` (may need --inplace as extra argument).
5. Copy so object from build/lib.*/ at the root of the od_mstar3 folder.
6. Check by going back to the root of the git folder, running python3 and `import cpp_mstar`

---

# To train PRIMAL:
Run: `python3 primal_train.py` or
submit batch job on Purdue scholar cluster with `sbatch strain.sh`

---

# To test:
Download the `saved_environments` [here](https://drive.google.com/file/d/193mv6mhlcu9Bqxs6hSMTfSk_1GrPAiNO/view?usp=sharing) and put under PRIMAL folder.
Download the pretrained model [here](https://drive.google.com/file/d/1s6Xo_0lmdivFUG0ImLChVTW4plURG-3u/view?usp=share_link) and put under PRIMAL folder.

### Testing PRIMAL:
Run: `python3 -u turtlebot3.py --alg primal --no-gui --n-tests 10`

### Testing CBS:
Run: `python3 -u turtlebot3.py --alg cbs --no-gui --n-tests 10`

---

# To see the the algorithm working on simulated turtlebot robots: 
1. Download the `saved_environments` [here](https://drive.google.com/file/d/193mv6mhlcu9Bqxs6hSMTfSk_1GrPAiNO/view?usp=sharing) and put under PRIMAL folder.
2. Download the pretrained model [here](https://drive.google.com/file/d/1s6Xo_0lmdivFUG0ImLChVTW4plURG-3u/view?usp=share_link) and put under PRIMAL folder.
3. Run: `python3 -u turtlebot3.py --alg primal --n-tests 10`

---

# To see the statistics:
1. Generated figures are stored in `/stats`
2. To generate new figures, run the above scripts for testing. See **Testing PRIMAL** and **Testing CBS**.
3. Run `python3 visualizer.py`