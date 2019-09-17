# Stable-Matching
An implementation of the Gale-Shapley algorithm under the condition that there are fewer proposing members. Utilized to match big-little pairs or mentor-mentee pairs given 2 csvs of preferences

## How to Use

This script takes in 2 parameters representing the filenames of the big choices and little choices respectively

Run
```bash
python3 match.py <big-list-filename> <little-list-filename>
```

If your lists are named `BigListChoices.csv` and `LittleListChoices.csv` respectively, you can just run

```bash
python3 match.py
```

## Important Notes

As of 9/16/19, if there are more littles than bigs, the algorithm will break (it attempts to match every little to a big. This is currently being patched)

There are 2 test samples `BigSample1.csv` and `LittleSample1.csv` included in the repository