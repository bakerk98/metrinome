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

metric_generator = FunctionCallPathComplexity(Log(display_output=False))
backup_generator = RecursivePathComplexity(Log(display_output=False))
for k in graphs:
    graph = graphs[k]
    try:
        with Timeout(10,"Timedout"):
            result = metric_generator.evaluate(graph,graphs)
    except TimeoutError:
        try:
            with Timeout(10,"Timedoutagain"):
                result = backup_generator.evaluate(graph,graphs)
            try:
                print(f"{graph.name}|{sympy.O(result[0])}|{result[0]}")
            except:
                print(f"{graph.name}|{result[0]}")
        except TimeoutError:
            print(f"{graph.name}|Timeout|Timeout")
        continue
    try:
        apc = result['rfcapc']
        print(f"{graph.name}|{sympy.O(apc)}|{apc}")
    except:
        print(f"{graph.name}|{apc}")
