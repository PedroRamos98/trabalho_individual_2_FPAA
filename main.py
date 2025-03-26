import matplotlib.pyplot as plt
import networkx as nx

def maxmin_select(arr, low, high, build_graph=False, G=None, parent=None, level=0):
    """
    Encontra simultaneamente o maior e o menor elemento em um array usando divisão e conquista.
    
    Args:
        arr (list): Lista de números
        low (int): Índice inicial do intervalo
        high (int): Índice final do intervalo
        build_graph (bool): Se True, constrói o grafo da recursão
        G (nx.DiGraph): Grafo para visualização (opcional)
        parent (str): ID do nó pai no grafo (opcional)
        level (int): Nível da recursão (opcional)
    
    Returns:
        tuple: (menor, maior) ou (menor, maior, G) se build_graph=True
    """
    # Inicializa o grafo apenas se build_graph for True
    if build_graph and G is None:
        G = nx.DiGraph()

    # Caso base 1: apenas um elemento
    if low == high:
        if build_graph:
            node_id = f"{low}-{high}"
            G.add_node(node_id, label=f"[{arr[low]}]\nMax={arr[low]}, Min={arr[low]}\nLevel {level}")
            if parent:
                G.add_edge(parent, node_id)
            return arr[low], arr[low], G
        return arr[low], arr[low]

    # Caso base 2: dois elementos
    if high == low + 1:
        if arr[low] < arr[high]:
            min_val, max_val = arr[low], arr[high]
        else:
            min_val, max_val = arr[high], arr[low]
        if build_graph:
            node_id = f"{low}-{high}"
            G.add_node(node_id, label=f"[{arr[low]}, {arr[high]}]\nMax={max_val}, Min={min_val}\n1 comp\nLevel {level}")
            if parent:
                G.add_edge(parent, node_id)
            return max_val, min_val, G
        return min_val, max_val

    # Divisão e conquista
    mid = (low + high) // 2
    if build_graph:
        node_id = f"{low}-{high}"
        G.add_node(node_id, label=f"[{', '.join(map(str, arr[low:high + 1]))}]\nLevel {level}")
        if parent:
            G.add_edge(parent, node_id)
        max_left, min_left, G = maxmin_select(arr, low, mid, build_graph, G, node_id, level + 1)
        max_right, min_right, G = maxmin_select(arr, mid + 1, high, build_graph, G, node_id, level + 1)
    else:
        max_left, min_left = maxmin_select(arr, low, mid, build_graph)
        max_right, min_right = maxmin_select(arr, mid + 1, high, build_graph)

    # Combinação
    final_min = min(min_left, min_right)
    final_max = max(max_left, max_right)
    
    if build_graph:
        G.nodes[node_id]['label'] = f"[{', '.join(map(str, arr[low:high + 1]))}]\nMax={final_max}, Min={final_min}\n2 comp\nLevel {level}"
        return final_max, final_min, G
    return final_min, final_max

def generate_diagram(G, filename="diagrama_maxmin.png"):
    """
    Gera e salva o diagrama da árvore de recursão.
    
    Args:
        G (nx.DiGraph): Grafo da recursão
        filename (str): Nome do arquivo para salvar o diagrama
    """
    pos = nx.spring_layout(G, k=0.5)  # Layout ajustado para melhor espaçamento
    labels = nx.get_node_attributes(G, 'label')
    plt.figure(figsize=(12, 8))  # Tamanho ajustável
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=3000, node_color='lightblue', 
            font_size=8, font_color='black', font_weight='bold', edge_color='gray')
    plt.savefig(filename, bbox_inches='tight')
    plt.close()

def test_maxmin_select():
    """
    Testa o algoritmo com diferentes casos, com e sem diagrama.
    """
    # Teste 1: Array com vários elementos (com diagrama)
    arr1 = [1000, 11, 445, 1, 330, 3000]
    min1, max1, G = maxmin_select(arr1, 0, len(arr1) - 1, build_graph=True)
    generate_diagram(G, "assets/diagrama_maxmin_test1.png")
    print(f"Teste 1 - Array: {arr1}")
    print(f"Menor: {min1}, Maior: {max1}")
    print("Diagrama salvo em 'assets/diagrama_maxmin_test1.png'")
    assert min1 == 1 and max1 == 3000, "Teste 1 falhou"

    # Teste 2: Array com um elemento (sem diagrama)
    arr2 = [42]
    min2, max2 = maxmin_select(arr2, 0, len(arr2) - 1)
    print(f"Teste 2 - Array: {arr2}")
    print(f"Menor: {min2}, Maior: {max2}")
    assert min2 == 42 and max2 == 42, "Teste 2 falhou"

    # Teste 3: Array com dois elementos (sem diagrama)
    arr3 = [5, 10]
    min3, max3 = maxmin_select(arr3, 0, len(arr3) - 1)
    print(f"Teste 3 - Array: {arr3}")
    print(f"Menor: {min3}, Maior: {max3}")
    assert min3 == 5 and max3 == 10, "Teste 3 falhou"

    print("Todos os testes passaram com sucesso!")

if __name__ == "__main__":
    test_maxmin_select()