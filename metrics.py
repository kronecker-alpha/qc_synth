"""read metrics from json file and calculate other metrics."""
import json
import os
from qiskit import QuantumCircuit
from circuits import gate_methods

#get all json files in results folder
root = "/Users/sophiekw/Desktop/project/qc_synth/results"
dir_list = os.listdir(root)

for file in dir_list:
    #open and load json
    file2 = os.path.join(root,file)
    with open(file2, "r") as fp:
        metrics = json.load(fp)
    final = metrics["circuit"]

    #basic metrics
    final_fidelity = metrics["ffidelity"]
    final_fitness = metrics["generations"][-1]["best_fitness"]
    time2 = metrics["time"]
    gate_set = metrics["gate_set"]

    #circuit metrics
    qis = QuantumCircuit(int(file[0])) #create circuit
    for gene in final:
        gate_methods[gene[0]](qis,gene[1], gene[2], gene[3], gene[4])
    circuit_depth = qis.depth()
    gate_count = qis.size()

    #evolutionary metrics
    #gens to 90% of best fitness
    threshold = 0.9 * final_fitness
    for gen in metrics["generations"]:
        if gen["best_fitness"] >= threshold:
            fit_90 = gen["generation"]
            break

    print(f"file: {file}\nfinal fidelity: {final_fidelity}\nfinal fitness: {final_fitness}")
    print(f"depth: {circuit_depth}\ngate count: {gate_count}\ngens to 90%: {fit_90}\nruntime: {time2}")
