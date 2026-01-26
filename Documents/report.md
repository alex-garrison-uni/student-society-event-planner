# Report

## Introduction

...

## Design and Approach

...

## Algorithms

### Brute-force

The brute-force algorithm finds an optimal solution for a given event by evaluating all possible valid subsets of the event activities. It does this through a recursive enumeration approach, with a modified depth first traversal of a binary decision tree. **A binary tree data structure is not implemented due to added memory overhead.**

A standard DFS approach has to be modified such that:
- The algorithm should populate nodes as they are traversed, not traverse an existing data structure
- It must evaluate and keep track of running totals such as the current enjoyment score and the time used
- It must check that subsets will not exceed the constraint

Data structures:
- Custom object types for Event and Activity (Python `class`)
- Dynamic arrays for chosen activities and possible event activities (Python `list`)
- Tuple for the function return values (Python `tuple`)

#### Pseudo-code
```
FUNCTION recursive_bruteforce(i, time_used, enjoyment, chosen_activities)
    IF i = number of activities THEN
        RETURN (chosen_activities, enjoyment, time_used)
    ENDIF

    best <- recursive_bruteforce(i + 1, time_used, enjoyment, chosen_activities)

    activity <- event.activities[i]
    new_time_used <- time_used + activity.time

    IF new_time_used <= event.max_time THEN
        take <- recursive_bruteforce(
            i + 1, 
            time_used + activity.time, 
            enjoyment + activity.enjoyment, 
            chosen_activities + [activity]
        )

        IF take.enjoyment > best.enjoyment
            best <- take
        ENDIF
    ENDIF

    RETURN best
```

To call `recursive_bruteforce` you need to supply the arguments `i = 0`, `time_used = 0`, `enjoyment = 0` and `chosen_activites = empty dynamic array`.

#### Efficiency

This algorithm evaluates, in the worst case, all possible subsets of the set of possible activities.  
$\left| \wp(\text{activities}) \right| = 2^n$, where $n$ is the number of elements in $\text{activities}$, and so the algorithm's worst case time complexity is $O(2^n)$ (exponential).

As the algorithm does not include activities which exceed the constraint, the search space will typically be much lower than $2^n$.

The algorithm's space complexity is linear as only one array is stored at a time, due to the DFS approach and that if an activity is taken, the space cost is only $O(n)$ due to one dynamic array creation operation. All subsets are not stored concurrently. 

## Testing and Results

...