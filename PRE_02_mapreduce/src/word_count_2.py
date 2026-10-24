"""Conteo de palabras con un simulador sencillo de Hadoop MapReduce."""

import glob
import os
import shutil
import string
from itertools import groupby
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def _resolve_existing(path):
    if os.path.exists(path):
        return path
    candidate = REPO_ROOT / path
    if candidate.exists():
        return str(candidate)
    raise FileNotFoundError(f"No se encontró la carpeta: {path}")


def _empty_folder(folder):
    for entry in os.listdir(folder):
        path = os.path.join(folder, entry)
        if os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=True)
        else:
            os.remove(path)


def initialize_folder(folder):
    if os.path.exists(folder):
        _empty_folder(folder)
    else:
        os.makedirs(folder)


def delete_folder(folder):
    if os.path.exists(folder):
        try:
            shutil.rmtree(folder)
        except PermissionError:
            _empty_folder(folder)


def generate_file_copies(input_folder, output_folder, n):
    input_folder = _resolve_existing(input_folder)
    os.makedirs(output_folder, exist_ok=True)
    for file in glob.glob(os.path.join(input_folder, "*")):
        if not os.path.isfile(file):
            continue
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()
        base, ext = os.path.splitext(os.path.basename(file))
        for i in range(1, n + 1):
            with open(os.path.join(output_folder, f"{base}_{i}{ext}"), "w", encoding="utf-8") as f:
                f.write(text)


def mapper(sequence):
    pairs = []
    table = str.maketrans("", "", string.punctuation)
    for _, line in sequence:
        line = line.lower().translate(table).replace("\n", "")
        pairs.extend((word, 1) for word in line.split())
    return pairs


def reducer(sequence):
    return [
        (key, sum(value for _, value in group))
        for key, group in groupby(sequence, key=lambda x: x[0])
    ]


def _read_input(input_folder):
    sequence = []
    for file in sorted(glob.glob(os.path.join(input_folder, "*"))):
        if not os.path.isfile(file):
            continue
        with open(file, "r", encoding="utf-8") as f:
            sequence.extend((file, line) for line in f)
    return sequence


def _write_output(output_folder, sequence):
    os.makedirs(output_folder, exist_ok=True)
    with open(os.path.join(output_folder, "part-00000"), "w", encoding="utf-8") as f:
        for key, value in sequence:
            f.write(f"{key}\t{value}\n")
    with open(os.path.join(output_folder, "_SUCCESS"), "w", encoding="utf-8") as f:
        f.write("")


def hadoop(input_folder, output_folder, mapper_fn, reducer_fn):
    sequence = _read_input(input_folder)
    sequence = mapper_fn(sequence)
    sequence = sorted(sequence, key=lambda x: x[0])
    sequence = reducer_fn(sequence)
    _write_output(output_folder, sequence)