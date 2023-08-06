from typing import List
import _kaldi_native_io
from _kaldi_native_io import (
    CompressionMethod,
    HtkHeader,
    MatrixShape,
    WaveData,
    WaveInfo,
    _DoubleMatrix as DoubleMatrix,
    _DoubleVector as DoubleVector,
    _FloatMatrix as FloatMatrix,
    _FloatVector as FloatVector,
    read_wave,
    read_wave_info,
)

from .table_types import (
    BoolWriter,
    CompressedMatrixWriter,
    DoubleMatrixWriter,
    DoubleVectorWriter,
    DoubleWriter,
    FloatMatrixWriter,
    FloatPairVectorWriter,
    FloatVectorWriter,
    FloatWriter,
    GaussPostWriter,
    HtkMatrixWriter,
    Int32PairVectorWriter,
    Int32VectorVectorWriter,
    Int32VectorWriter,
    Int32Writer,
    PosteriorWriter,
    RandomAccessBoolReader,
    RandomAccessDoubleMatrixReader,
    RandomAccessDoubleReader,
    RandomAccessDoubleVectorReader,
    RandomAccessFloatMatrixReader,
    RandomAccessFloatPairVectorReader,
    RandomAccessFloatReader,
    RandomAccessFloatVectorReader,
    RandomAccessGaussPostReader,
    RandomAccessHtkMatrixReader,
    RandomAccessInt32PairVectorReader,
    RandomAccessInt32Reader,
    RandomAccessInt32VectorReader,
    RandomAccessInt32VectorVectorReader,
    RandomAccessMatrixShapeReader,
    RandomAccessPosteriorReader,
    RandomAccessTokenReader,
    RandomAccessTokenVectorReader,
    RandomAccessWaveInfoReader,
    RandomAccessWaveReader,
    SequentialBoolReader,
    SequentialDoubleMatrixReader,
    SequentialDoubleReader,
    SequentialDoubleVectorReader,
    SequentialFloatMatrixReader,
    SequentialFloatPairVectorReader,
    SequentialFloatReader,
    SequentialFloatVectorReader,
    SequentialGaussPostReader,
    SequentialHtkMatrixReader,
    SequentialInt32PairVectorReader,
    SequentialInt32Reader,
    SequentialInt32VectorReader,
    SequentialInt32VectorVectorReader,
    SequentialMatrixShapeReader,
    SequentialPosteriorReader,
    SequentialTokenReader,
    SequentialTokenVectorReader,
    SequentialWaveInfoReader,
    SequentialWaveReader,
    TokenVectorWriter,
    TokenWriter,
)

from pathlib import Path as _Path

cmake_prefix_path = _Path(__file__).parent / "share" / "cmake"
del _Path


def read_int32_vector(rxfilename: str) -> List[int]:
    """Read a vector of int32 from an rxfilename"""
    return _kaldi_native_io.read_int32_vector(rxfilename)
__version__ = '1.16'
