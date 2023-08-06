from pulp import LpStatus

__all__ = ['report_result']


def report_result(model):
    """
    Utility function to simplify PuLP result parsing
    """
    result = {
        "solver": model.solver.name,
        "optimization_result": {
            model.objective.name: model.objective.value(),
            "status": LpStatus[model.status]
        },
        "constraint_sensitivity": [
            {'name': name, 'constraint': str(c), 'activity': c.value() - c.constant, 'slack': c.slack}
            if model.isMIP() else 
            {'name': name, 'constraint': str(c), 'marginal': c.pi, 'activity': c.value() - c.constant, 'slack': c.slack}
            for name, c in model.constraints.items()
        ]
    }
    for v in model.variables(): 
        result["optimization_result"][v.name] = v.varValue
    return result
