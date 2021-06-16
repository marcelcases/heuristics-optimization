# Heuristic Optimization

## About

**Course**  
Algorithmic Methods for Mathematical Models (AMMM-MIRI)  
FIB - Universitat Politècnica de Catalunya. BarcelonaTech  
Spring 2021

**Team**  
* Marc Catrisse
&lt;marc.catrisse@estudiantat.upc.edu&gt;
* Marcel Cases
&lt;marcel.cases@estudiantat.upc.edu&gt;

## Statement

In a scientific conference, the program chair (PC) is in charge of scheduling the different talks. Scheduling a talk means assigning a room and a time slot to it. The PC is particularly concerned about the way talks on related topics are scheduled.

More precisely, we have a set of n talks N = {1,2,...,n} and two symmetric Boolean matrices Pij and Sij such that respectively Pij = 1 if and only if talks i and j are primarily related, and Sij = 1 if and only if talks i and j are secondarily related. The input guarantees that any two talks cannot be both primarily and secondarily related; that is, for any 1 ≤ i ≤ j ≤ n, it cannot be the case that Pij = 1 and Sij = 1. For convenience, it is ensured that the matrices also satisfy that Pii = Sii = 0 for all 1 ≤ i ≤ n.

For our purposes, the conference consists of a sequence of t time slots T = {1,2,...,t} and a sequence of r lecture rooms R = {1,2,...,r} that can be used in parallel during all time slots. A conference program is an assignment of a lecture room and a time slot to each talk so that two different talks are not assigned the same room at the same time. The number of talks n, the number of time slots t and the number of lecture rooms r satisfy that 0 < n ≤ t × r.

A conference program has to satisfy some additional constraints in order to be valid. Namely, any two primarily related talks cannot be scheduled at the same time. On the other hand, it is not allowed that such talks are scheduled too far apart either: the time distance between two primarily related talks should be at most d, where this parameter is part of the input and satisfies 0 < d < t. E.g., if d = 1 and talks 3 and 4 are primarily related, then they cannot be scheduled at time slots 2 and 5 respectively, as their time distance would be 5 − 2 = 3 > 1.

Finally, we measure the cost of a valid program by the number of different pairs of talks that are secondarily related and scheduled at the same time. The goal of this project is to find a valid conference program that minimizes this quantity.

## Solvers

The following solvers have been developed to optimize the cost of this problem:
* [Greedy](Heuristics/solvers/solver_Greedy.py)
* [Local Search](Heuristics/solvers/localSearch.py)
* [GRASP](Heuristics/solvers/solver_GRASP.py)

## Instances

You can use the [Instance Generator](Instances/InstanceGenerator.py) to generate random instances to be solved using any of the solvers.

Configure the parameters of the instance to be generated on [heuristics-optimization/Instances/config/config.dat](heuristics-optimization/Instances/config/config.dat)

For setting the density of 1s in primarily and secondarily related talks, modify variable `p` on [InstanceGenerator.py](Instances/InstanceGenerator.py). Notice that this has an impact on the feasibility of the instances, as well as the complexity for the solver.

For running the generator, run `python Main.py`.

## Run the solver

Put the instances previously generated in [Heuristics/data](Heuristics/data).

Set up the [configuration file](Heuristics/config/config.dat).

Run `python Main.py`.

## Solutions

The solutions obtained, in case there are some, will be stored on [Heuristics/solvers](Heuristics/solvers).
