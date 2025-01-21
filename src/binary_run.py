from core.log import Log
from metric.fcn_call_path_complexity import FunctionCallPathComplexity
from metric.recursive_path_complexity import RecursivePathComplexity
from graph.control_flow_graph import ControlFlowGraph, Metadata
from graph.graph import EdgeListGraph
from core.env import Env, KnownExtensions
from utils import Timeout
import os,sys
import sympy
import traceback

#this script will return the "biggest" between path complexities of function path complexity and recursive path complexity

files = sys.argv[1:]
#print(files)
for f in files:
    if not os.path.isfile(f):
        print(f"Invalid path: {f}")
        sys.exit(1)

graphs = {}
for f in files:
    graph_name = os.path.basename(f)
    #    try:
    graph = ControlFlowGraph.from_file(f, EdgeListGraph,
                                           [Metadata.with_language(KnownExtensions.C)])
    # except ValueError as e:
    #     print(f"value error with {f}")
    #     with open(f,"r") as b:
    #         print(b.read())
    #     print(traceback.format_exc())
    #     sys.exit(1)
    graphs[graph_name] = graph

fun_call_generator = FunctionCallPathComplexity(Log(display_output=False))
recursive_generator = RecursivePathComplexity(Log(display_output=False))

for k in graphs:
    graph = graphs[k]
    recursiveCalls = False
    results = []
    for node in graph.metadata.calls.keys():
        if graph.metadata.calls[node].split()[1] == graph.name.split(".")[1]:
            recursiveCalls = True
            break
    #using a 10 second timeout, try to get the apc from both metrics if necessary
    try:
        with Timeout(10,"Timedout"):
            if recursiveCalls:
                results.append(recursive_generator.evaluate(graph))
        with Timeout(10,"Timedout"):
            results.append(fun_call_generator.evaluate(graph,graphs)['rfcapc'])
    #if we timeout, return timeout, if we error, "return" error
    except TimeoutError:
        print(f"{graph.name}|Timeout")
        continue
    except:
        print(f"{graph.name}|Error")
        continue
    #try and print the apc with sympy big o notation,
    #Otherwise just print the apc results
    if len(results) > 1:
        #figure out which is bigger and return that
        big_o_results = []
        for res in results:
            try:
                big_o_results.append(sympy.O(res))
            except:
                big_o_results.append(res)
        # biggest = ord1
        # if ord2 in ord1:
        #     biggest = ord2
        # print(f"biggest: {biggest}")
        biggest = big_o_results[0]
        if big_o_results[1] in big_o_results[0]:
            biggest = big_o_results[1]
        print(f"{graph.name}|{biggest}")
    else:
        try:
            res = sympy.O(results[0])
            print(f"{graph.name}|{res}")
        except:
            print(f"{graph.name}|{results[0]}")
