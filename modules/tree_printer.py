from __future__ import annotations

from typing import Any
from rich.tree import Tree
from rich.console import Console
from modules.ply_lex import LexToken
import modules.rd_parcer.sujeto as Sujeto
import modules.rd_parcer.verbo as Verbo
import modules.rd_parcer.complemento as Complemento
import modules.rd_parcer.oraciones as Oraciones


def _format_token(tok: LexToken) -> str:
    if tok is None:
        return "None"
    # Mostramos tipo y valor: TIPO(valor)
    try:
        tname = tok.type.name
    except AttributeError:
        tname = str(tok.type)
    return f"{tname}({tok.value})"


def _node_label(node: Any) -> str:
    # Etiquetas amigables según el tipo de nodo
    if isinstance(node, Oraciones.OracionSVO):
        return "OracionSVO"
    if isinstance(node, Sujeto.Sujetos):
        return "Sujetos"
    if isinstance(node, Sujeto.SujetoDet):
        return "SujetoDet"
    if isinstance(node, Sujeto.Nombre):
        return "Nombre"
    if isinstance(node, Verbo.Verbo):
        return "Verbo"
    if isinstance(node, Complemento.ComplementoPre):
        return "ComplementoPre"
    if isinstance(node, LexToken):
        return _format_token(node)
    if node is None:
        return "None"
    return type(node).__name__


def _children_of(node: Any) -> list[tuple[str, Any]]:
    """Devuelve una lista de pares (etiqueta_relacion, hijo) para construir el árbol."""
    children: list[tuple[str, Any]] = []

    if isinstance(node, list):
        for i, elem in enumerate(node):
            children.append((f"[{i}]", elem))
        return children

    if isinstance(node, Oraciones.OracionSVO):
        children.append(("sujeto", node.sujeto))
        children.append(("verbo", node.verbo))
        children.append(("complemento", node.complemento))
        return children

    if isinstance(node, Sujeto.Sujetos):
        for i, s in enumerate(node.sujetos):
            children.append((f"sujetos[{i}]", s))
        return children

    if isinstance(node, Sujeto.SujetoDet):
        children.append(("determinante", node.determinante))
        children.append(("sustantivo", node.sustantivo))
        children.append(("adjetivo", node.adjetivo))
        return children

    if isinstance(node, Sujeto.Nombre):
        children.append(("nombre", node.nombre))
        children.append(("adjetivo", node.adjetivo))
        return children

    if isinstance(node, Verbo.Verbo):
        children.append(("negacion", node.negacion))
        children.append(("verbo", node.verbo))
        children.append(("objeto", node.objeto))
        # Adverbios (lista)
        for i, adv in enumerate(getattr(node, "adverbios", []) or []):
            children.append((f"adverbio[{i}]", adv))
        return children

    if isinstance(node, Complemento.ComplementoPre):
        children.append(("preposicion", node.preposicion))
        children.append(("sujeto", node.sujeto))
        return children

    # LexToken o None no tienen hijos
    return children


def _build_subtree(node: Any, label: str | None = None) -> Tree:
    """Construye un árbol de rich.Tree a partir de un nodo del AST."""
    node_label = _node_label(node)
    if label is not None:
        root = Tree(f"{label}: {node_label}")
    else:
        root = Tree(node_label)

    for rel, child in _children_of(node):
        child_label = f"{rel}: {_node_label(child)}"
        child_branch = root.add(child_label)
        # Llamada recursiva solo si el hijo tiene a su vez hijos
        if _children_of(child):
            _add_children(child_branch, child)

    return root


def _add_children(tree_node: Tree, node: Any) -> None:
    for rel, child in _children_of(node):
        child_label = f"{rel}: {_node_label(child)}"
        child_branch = tree_node.add(child_label)
        if _children_of(child):
            _add_children(child_branch, child)


def print_tree(root: Any) -> None:
    """Imprime el árbol de análisis sintáctico usando rich.Tree.

    - Si `root` es una lista de oraciones (párrafo), se imprime una raíz
      "Árbol de análisis sintáctico <list>" y un subárbol por oración.
    - Si es un solo nodo, se imprime directamente.
    """
    console = Console()

    if isinstance(root, list):
        main_tree = Tree("Árbol de análisis sintáctico <list>")
        for i, node in enumerate(root):
            subtree = _build_subtree(node, label=f"[{i}]")
            main_tree.add(subtree)
        console.print(main_tree)
    else:
        tree = _build_subtree(root)
        console.print(tree)
