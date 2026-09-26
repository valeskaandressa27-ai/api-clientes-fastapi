"""Exceções de domínio, desacopladas do framework web."""


class ClienteNaoEncontradoError(Exception):
    """Levantada quando um cliente não é encontrado pelo ID informado."""


class EmailDuplicadoError(Exception):
    """Levantada quando já existe um cliente cadastrado com o mesmo e-mail."""


class CpfDuplicadoError(Exception):
    """Levantada quando já existe um cliente cadastrado com o mesmo CPF."""
