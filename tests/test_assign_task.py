# import pytest
# from app.logic.chore_distribution import split_list_to_groups  # Import the actual function from your bot file

# def test_split_list_to_groups():
#     tasks = [
#         {'name': 'task1', 'complexity': 3}, 
#         {'name': 'task2', 'complexity': 1}, 
#         {'name': 'task3', 'complexity': 5}, 
#         {'name': 'task5', 'complexity': 2}, 
#         {'name': 'task12', 'complexity': 4}, 
#         {'name': 'puk', 'complexity': 3}, 
#         {'name': 'sruk', 'complexity': 2}, 
#         {'name': 'вонь', 'complexity': 1}, 
#         {'name': 'говонь', 'complexity': 5}
#     ]
#     persons = [
#         {'id': 1, 'name': 'Alice'}, 
#         {'id': 2, 'name': 'Bob'}, 
#         {'id': 3, 'name': 'Charlie'}
#     ]
    
#     result = split_list_to_groups(tasks, persons)
    
#     # Ensure that all tasks are assigned
#     assigned_tasks = sum(len(group['tasks']) for group in result)
#     assert assigned_tasks == len(tasks), "Not all tasks were assigned!"
    
#     # Check that each person received at least one task
#     for group in result:
#         assert len(group['tasks']) > 0, f"Person {group['person']['name']} received no tasks!"
    
#     # Check that tasks are distributed fairly by complexity
#     complexities = [sum(task['complexity'] for task in group['tasks']) for group in result]
#     max_complexity = max(complexities)
#     min_complexity = min(complexities)
#     assert max_complexity - min_complexity <= 2, "Complexities are not fairly distributed!"
