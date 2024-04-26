
import pickle


# Node definition
def create_node(leaf=False):
    return {'keys': [], 'children': [], 'data': [], 'leaf': leaf}

# BTree initialization
def initialize_b_tree(t):
    return {'root': create_node(True), 't': t}

# Search function
def search_b_tree(b_tree, key, node = None):
    if node is None:
        node = b_tree['root']  
    else:
        node
    i = 0
    while i < len(node['keys']) and key > node['keys'][i]:
        i += 1
    if i < len(node['keys']) and key == node['keys'][i]:
        return (key, node['data'][i])
    elif node['leaf']:
        return None
    else:
        return search_b_tree(b_tree, key, node['children'][i])

# Split Child function
def split_child(b_tree, parent_node, child_index):
    t = b_tree['t']

    # Child node to split
    child_node = parent_node['children'][child_index]

    # Create a new node and add it to the parent's list of children
    new_child_node = create_node(child_node['leaf'])
    parent_node['children'].insert(child_index + 1, new_child_node)

    # Insert the median of the full child into the parent
    parent_node['keys'].insert(child_index, child_node['keys'][t - 1])
    parent_node['data'].insert(child_index, child_node['data'][t - 1])

    # Split the keys and data of the full child between the old and new child
    new_child_node['keys'] = child_node['keys'][t: (2 * t) - 1]
    new_child_node['data'] = child_node['data'][t: (2 * t) - 1]
    child_node['keys'] = child_node['keys'][0: t - 1]
    child_node['data'] = child_node['data'][0: t - 1]

    # If the child is not a leaf, reassign its children to the old and new child
    if not child_node['leaf']:
        new_child_node['children'] = child_node['children'][t: 2 * t]
        child_node['children'] = child_node['children'][0: t]

# Insert function
def insert_b_tree(b_tree, key, data):
    t = b_tree['t']
    root = b_tree['root']

    # If root is full, create a new node - tree's height grows by 1
    if len(root['keys']) == (2 * t) - 1:
        new_root = create_node()
        b_tree['root'] = new_root
        new_root['children'].insert(0, root)
        split_child(b_tree, new_root, 0)
        insert_non_full_b_tree(b_tree, new_root, key, data)
    else:
        insert_non_full_b_tree(b_tree, root, key, data)

# Insert Non-Full function
def insert_non_full_b_tree(b_tree, node, key, data):
    t = b_tree['t']
    i = len(node['keys']) - 1

    # Find the correct spot in the leaf to insert the key
    if node['leaf']:
        node['keys'].append(None)
        node['data'].append(None)
        while i >= 0 and key < node['keys'][i]:
            node['keys'][i + 1] = node['keys'][i]
            node['data'][i + 1] = node['data'][i]
            i -= 1
        node['keys'][i + 1] = key
        node['data'][i + 1] = data
    # If not a leaf, find the correct subtree to insert the key
    else:
        while i >= 0 and key < node['keys'][i]:
            i -= 1
        i += 1
        # If child node is full, split it
        if len(node['children'][i]['keys']) == (2 * t) - 1:
            split_child(b_tree, node, i)
            if key > node['keys'][i]:
                i += 1
        insert_non_full_b_tree(b_tree, node['children'][i], key, data)


# Delete function
def delete_b_tree(b_tree, node, key):
    t = b_tree['t']
    i = 0
    while i < len(node['keys']) and key > node['keys'][i]:
        i += 1
    if node['leaf']:
        if i < len(node['keys']) and node['keys'][i] == key:
            # Delete key and corresponding data from leaf node
            node['keys'].pop(i)
            node['data'].pop(i)
        return
    if i < len(node['keys']) and node['keys'][i] == key:
        # Delete key from internal node
        return delete_internal_node_b_tree(b_tree, node, key, i)
    elif len(node['children'][i]['keys']) >= t:
        # Key to be deleted is in the subtree rooted at children[i]
        delete_b_tree(b_tree, node['children'][i], key)
    else:
        # Key to be deleted is not in the subtree rooted at children[i]
        # Perform necessary operations to balance the tree
        if i != 0 and i + 2 < len(node['children']):
            if len(node['children'][i - 1]['keys']) >= t:
                delete_sibling_b_tree(b_tree, node, i, i - 1)
            elif len(node['children'][i + 1]['keys']) >= t:
                delete_sibling_b_tree(b_tree, node, i, i + 1)
            else:
                delete_merge_b_tree(b_tree, node, i, i + 1)
        elif i == 0:
            if len(node['children'][i + 1]['keys']) >= t:
                delete_sibling_b_tree(b_tree, node, i, i + 1)
            else:
                delete_merge_b_tree(b_tree, node, i, i + 1)
        elif i + 1 == len(node['children']):
            if len(node['children'][i - 1]['keys']) >= t:
                delete_sibling_b_tree(b_tree, node, i, i - 1)
            else:
                delete_merge_b_tree(b_tree, node, i, i - 1)
        delete_b_tree(b_tree, node['children'][i], key)

# Delete Internal Node function
def delete_internal_node_b_tree(b_tree, node, key, index):
    t = b_tree['t']
    if node['leaf']:
        # If the node is a leaf, delete the key and return None
        if node['keys'][index] == key:
            node['keys'].pop(index)
            node['data'].pop(index)
        return None
    if len(node['children'][index]['keys']) >= t:
        # If the child that precedes the key has at least t keys,
        # find the predecessor of the key in the subtree rooted at that child
        deleted_key = delete_predecessor_b_tree(b_tree, node['children'][index])
        return deleted_key
    elif len(node['children'][index + 1]['keys']) >= t:
        # If the child that succeeds the key has at least t keys,
        # find the successor of the key in the subtree rooted at that child
        deleted_key = delete_successor_b_tree(b_tree, node['children'][index + 1])
        return deleted_key
    else:
        # Merge the child that contains the key and its right sibling
        delete_merge_b_tree(b_tree, node, index, index + 1)
        # Recursively delete the key from the merged child
        return delete_internal_node_b_tree(b_tree, node['children'][index], key, t - 1)

# Delete Predecessor function
def delete_predecessor_b_tree(b_tree, node):
    t = b_tree['t']
    if node['leaf']:
        # If the node is a leaf, delete its rightmost key
        return node['keys'].pop(), node['data'].pop()
    n = len(node['keys']) - 1
    if len(node['children'][n]['keys']) >= t:
        # If the rightmost child of the node has at least t keys,
        # recursively delete the predecessor from that child
        delete_sibling_b_tree(b_tree, node, n + 1, n)
    else:
        # Merge the rightmost child with its right sibling
        delete_merge_b_tree(b_tree, node, n, n + 1)
    # Recursively find and delete the predecessor in the merged child
    return delete_predecessor_b_tree(b_tree, node['children'][n])

# Delete Successor function
def delete_successor_b_tree(b_tree, node):
    t = b_tree['t']
    if node['leaf']:
        # If the node is a leaf, delete its leftmost key
        return node['keys'].pop(0), node['data'].pop(0)
    if len(node['children'][1]['keys']) >= t:
        # If the leftmost child of the node has at least t keys,
        # recursively delete the successor from that child
        delete_sibling_b_tree(b_tree, node, 0, 1)
    else:
        # Merge the leftmost child with its right sibling
        delete_merge_b_tree(b_tree, node, 0, 1)
    # Recursively find and delete the successor in the merged child
    return delete_successor_b_tree(b_tree, node['children'][0])

# Delete Merge function
def delete_merge_b_tree(b_tree, node, index, sibling_index):
    # Retrieve the child node and its sibling
    child_node = node['children'][index]
    if sibling_index > index:
        # If the sibling is to the right of the child
        sibling_node = node['children'][sibling_index]
        # Move the key from the parent node to the child node
        child_node['keys'].append(node['keys'][index])
        child_node['data'].append(node['data'][index])
        # Merge keys and data from the sibling node into the child node
        child_node['keys'] += sibling_node['keys']
        child_node['data'] += sibling_node['data']
        # If the sibling node has children, move its children to the child node
        if len(sibling_node['children']) > 0:
            child_node['children'] += sibling_node['children']
        # Remove the key from the parent node and the sibling node
        node['keys'].pop(index)
        node['data'].pop(index)
        node['children'].pop(sibling_index)
    else:
        # If the sibling is to the left of the child
        sibling_node = node['children'][sibling_index]
        # Move the key from the parent node to the sibling node
        sibling_node['keys'].insert(0, node['keys'][index - 1])
        sibling_node['data'].insert(0, node['data'][index - 1])
        # Merge keys and data from the child node into the sibling node
        sibling_node['keys'] = child_node['keys'] + sibling_node['keys']
        sibling_node['data'] = child_node['data'] + sibling_node['data']
        # If the child node has children, move its children to the sibling node
        if len(child_node['children']) > 0:
            sibling_node['children'] = child_node['children'] + sibling_node['children']
        # Remove the key from the parent node and the child node
        node['keys'].pop(index - 1)
        node['data'].pop(index - 1)
        node['children'].pop(index)




def delete_sibling_b_tree(b_tree, node, index, sibling_index):
    child_node = node['children'][index]
    if index < sibling_index:
        # If the sibling node is to the right of the child node
        sibling_node = node['children'][sibling_index]
        # Move the key from the parent node to the child node
        child_node['keys'].append(node['keys'][index])
        child_node['data'].append(node['data'][index])
        # Move the key from the sibling node to the parent node
        node['keys'][index] = sibling_node['keys'].pop(0)
        node['data'][index] = sibling_node['data'].pop(0)
        # If the sibling node has children, move its first child to the child node
        if len(sibling_node['children']) > 0:
            child_node['children'].append(sibling_node['children'].pop(0))
    else:
        # If the sibling node is to the left of the child node
        sibling_node = node['children'][sibling_index]
        # Move the key from the parent node to the sibling node
        sibling_node['keys'].insert(0, node['keys'][index - 1])
        sibling_node['data'].insert(0, node['data'][index - 1])
        # Move the key from the sibling node to the parent node
        node['keys'][index - 1] = sibling_node['keys'].pop()
        node['data'][index - 1] = sibling_node['data'].pop()
        # If the sibling node has children, move its last child to the child node
        if len(sibling_node['children']) > 0:
            child_node['children'].insert(0, sibling_node['children'].pop())





# Print Tree function
def print_tree_b_tree(node, level=0):
    # Print keys and data of the current node at the specified level
    print(f'Level {level}', end=": ")
    for i in range(len(node['keys'])):
        print(f"({node['keys'][i]}, {node['data'][i]})", end=" ")
    print()
    level += 1
    # Recursively print the tree for each child node
    if len(node['children']) > 0:
        for child_node in node['children']:
            print_tree_b_tree(child_node, level)





def inorder_traversal(b_tree, node=None, visited=None):
    # Initialize node and visited set if not provided
    if node is None:
        node = b_tree['root']
    if visited is None:
        visited = set()

    result = []
    # Traverse the tree in inorder manner
    if not node['leaf']:
        for i in range(len(node['children'])):
            result += inorder_traversal(b_tree, node['children'][i], visited)
            if i < len(node['keys']):
                # Visit the current key if not already visited
                if node['keys'][i] not in visited:
                    result.append((node['keys'][i], node['data'][i]))
                    visited.add(node['keys'][i])
    else:
        for i in range(len(node['keys'])):
            # Visit the current key if not already visited
            if node['keys'][i] not in visited:
                result.append((node['keys'][i], node['data'][i]))
                visited.add(node['keys'][i])

    return result

def update(b_tree, key, new_data):
    # Extracting parameters from the B-tree dictionary
    t = b_tree['t']
    x = b_tree['root']

    # Traverse the B-tree to find the node containing the key
    while True:
        i = 0
        # Find the appropriate position for the key in the current node
        while i < len(x['keys']) and key > x['keys'][i]:
            i += 1

        # If the key is found in the current node, update its data
        if i < len(x['keys']) and key == x['keys'][i]:
            x['data'][i] = new_data
            return

        # If the current node is a leaf, the key does not exist in the tree
        if x['leaf']:
            break

        # Move to the child node for further search
        x = x['children'][i]

    # If the node is not full, insert the key and data into it
    
    if t <= len(x['keys']) < 2 * t:
        i = len(x['keys']) - 1
        # Find the appropriate position for the new key
        while i >= 0 and key > x['keys'][i]:
            x['keys'][i + 1] = x['keys'][i]
            x['data'][i + 1] = x['data'][i]
            i -= 1
        # Insert the new key and data into the node
        x['keys'][i + 1] = key
        x['data'][i + 1] = new_data

    # If the node is full, split it and recursively update the tree
    else:
        split_child(b_tree, x, i + 1)
        # Determine which split part to traverse
        if key > x['keys'][i + 1]:
            i += 1
        # Recursively update the B-tree with the new key and data
        update(b_tree, key, new_data)



EMP_DATA = initialize_b_tree(3)
    
# i = 0
# with open('myApp//input.txt', 'r') as file:
#         for line in file:
#             data = eval(line.strip())  # Read each line as a dictionary
#             x = str("0"*(6-len(str(i))) + str(i))
#             insert_b_tree(EMP_DATA, x, data)
#             i += 1
    
    
def insert_and_search_example():           
    update(EMP_DATA ,'000000', {'id': 'eeb87ea3', 'name': 'Jeffrey Walker',
                               'dob': '23-02-2014', 'address': 'Sherrifort', 
                               'email': 'ashleyterrell@example.net', 
                               'position': 'Camera operator', 'salary': 44752000})        
    print(print_tree_b_tree(EMP_DATA["root"]))

    B = EMP_DATA
    
    # Print the B-tree before deletion
    print("B-tree before deletion:")
    print(print_tree_b_tree(B['root']))
    print()
    print(inorder_traversal(B))
    # Delete key 8
    key_to_delete = "000000"
    print(f"Deleting key {key_to_delete} from the B-tree...")
    delete_b_tree(B, B['root'] ,key_to_delete)
    print(print_tree_b_tree(B['root']))
    print(inorder_traversal(B))
    # Print the B-tree after deletion
    print("\nB-tree after deleting key 000000:")

    print(print_tree_b_tree(B['root']))
    print()
    
    print('search')
    print(search_b_tree(B, "000001"))





def main():
    print('\n--- INSERT & SEARCH ---\n')
    # insert_and_search_example()
# 

# main()


# # Serialize B-tree to file
# def serialize_b_tree(b_tree, filename):
#     with open(filename, 'wb') as file:
#         pickle.dump(b_tree, file)


# # Deserialize B-tree from file
# def deserialize_b_tree(filename):
#     with open(filename, 'rb') as file:
#         return pickle.load(file)
