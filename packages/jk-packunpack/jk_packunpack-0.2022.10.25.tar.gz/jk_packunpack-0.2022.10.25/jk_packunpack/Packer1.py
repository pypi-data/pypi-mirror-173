
from genericpath import samestat
import os
import typing
import tarfile
import gzip
import bz2
import lzma

import jk_simpleexec
import jk_logging
import jk_utils

from .Spooler import Spooler
from .SpoolInfo import SpoolInfo






class Packer1(object):

	_TAR_PATH = "/bin/tar"

	################################################################################################################################
	## Static Helper Methods
	################################################################################################################################

	@staticmethod
	def _compressGZip(
			inFilePath:str,
			outFilePath:str,
			chModValueI:int = None,
			terminationFlag:jk_utils.TerminationFlag = None
		):

		assert inFilePath != outFilePath

		with open(inFilePath, "rb") as fin:
			if chModValueI is None:
				with gzip.open(outFilePath, "wb") as fout:
					Spooler.spoolStream(fin, fout, terminationFlag)
			else:
				fdesc = os.open(outFilePath, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, chModValueI)
				with open(fdesc, "wb") as fout2:
					with gzip.open(fout2, "wb") as fout:
						Spooler.spoolStream(fin, fout, terminationFlag)
	#

	@staticmethod
	def _compressBZip2(
			inFilePath:str,
			outFilePath:str,
			chModValueI:int = None,
			terminationFlag:jk_utils.TerminationFlag = None
		):

		assert inFilePath != outFilePath

		with open(inFilePath, "rb") as fin:
			if chModValueI is None:
				with bz2.open(outFilePath, "wb") as fout:
					Spooler.spoolStream(fin, fout, terminationFlag)
			else:
				fdesc = os.open(outFilePath, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, chModValueI)
				with open(fdesc, "wb") as fout2:
					with bz2.open(fout2, "wb") as fout:
						Spooler.spoolStream(fin, fout, terminationFlag)
	#

	@staticmethod
	def _compressXZ(
			inFilePath:str,
			outFilePath:str,
			chModValueI:int = None,
			terminationFlag:jk_utils.TerminationFlag = None
		):

		assert inFilePath != outFilePath

		with open(inFilePath, "rb") as fin:
			if chModValueI is None:
				with lzma.open(outFilePath, "wb") as fout:
					Spooler.spoolStream(fin, fout, terminationFlag)
			else:
				fdesc = os.open(outFilePath, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, chModValueI)
				with open(fdesc, "wb") as fout2:
					with lzma.open(fout2, "wb") as fout:
						Spooler.spoolStream(fin, fout, terminationFlag)
	#

	#
	# @return		str name
	# @return		str ext
	# @return		callable m
	#
	@staticmethod
	def _getCompressionParams(compression:str):
		assert isinstance(compression, str)

		if compression in [ "gz", "gzip" ]:
			return "gzip", ".gz", Packer1._compressGZip
		elif compression in [ "bz2", "bzip2" ]:
			return "bzip2", ".bz2", Packer1._compressBZip2
		elif compression in [ "xz" ]:
			return "xz", ".xz", Packer1._compressXZ
		else:
			raise Exception("Unknown compression: " + repr(compression))
	#

	################################################################################################################################
	## Static Public Methods
	################################################################################################################################

	#
	# Pack the specified directory in a tar file.
	#
	# @param		str srcDirPath						(required) The directory to pack
	# @param		str destTarFilePath					(required) The tar file to create
	# @param		AbstractLogger log					(required) A logger to write log information to
	#
	@staticmethod
	def tarDir(
			srcDirPath:str,
			destTarFilePath:str,
			log:jk_logging.AbstractLogger
		) -> str:
		return Packer1.tarDir2(
			srcDirPath,
			destTarFilePath,
			None,
			log)
	#

	#
	# Pack the specified directory in a tar file.
	#
	# @param		str srcDirPath						(required) The directory to pack
	# @param		str destTarFilePath					(required) The tar file to create
	# @param		AbstractLogger log					(required) A logger to write log information to
	#
	@staticmethod
	def tarDir2(
			*args,
			srcDirPath:str,
			destTarFilePath:str,
			chModValue:typing.Union[int,str,jk_utils.ChModValue,None] = None,
			log:jk_logging.AbstractLogger,
		) -> str:

		if args:
			raise Exception("Invoke this method with named arguments only!")

		assert isinstance(srcDirPath, str)
		assert isinstance(destTarFilePath, str)
		chModValue = jk_utils.ChModValue.createN(chModValue)
		chModValueI = None if chModValue is None else chModValue.toInt()
		assert isinstance(log, jk_logging.AbstractLogger)

		# ----

		with log.descend("Packing " + repr(srcDirPath) + " ...") as log2:
			srcDirPath = os.path.abspath(srcDirPath)
			assert os.path.isdir(srcDirPath)
			destTarFilePath = os.path.abspath(destTarFilePath)

			if not os.path.isfile(Packer1._TAR_PATH):
				raise Exception("'tar' not found!")

			tarArgs = [
				"-cf", destTarFilePath, "."
			]

			log2.notice("Invoking /bin/tar with: " + str(tarArgs))
			_oldmask = os.umask(0o777 ^ chModValueI) if chModValueI is not None else None
			try:
				cmdResult = jk_simpleexec.invokeCmd2(
					cmdPath=Packer1._TAR_PATH,
					cmdArgs=tarArgs,
					workingDirectory=srcDirPath,
				)
			finally:
				if _oldmask is not None:
					os.umask(_oldmask)
					os.chmod(destTarFilePath, chModValueI)	# required as tar will not set the execute bit

			if cmdResult.returnCode != 0:
				cmdResult.dump(printFunc=log2.error)
				raise Exception("Failed to run 'tar'!")

		return destTarFilePath
	#

	#
	# Pack the contents of the specified directory in a tar file.
	#
	# @param	str srcDirPath						(required) The directory to pack
	# @param	str destTarFilePath					(required) The tar file to create
	# @param	str[] filesAndDirsToInclude			(optional) The file and directorie names (without path!) to include.
	#												If <c>None</c> is specified the source directory is scanned and all
	#												files and directories found there will be included automatically.
	# @param	AbstractLogger log					(required) A logger to write log information to
	#
	@staticmethod
	def tarDirContents(
			*args,
			srcDirPath:str,
			destTarFilePath:str,
			chModValue:typing.Union[int,str,jk_utils.ChModValue,None] = None,
			filesAndDirsToInclude:typing.List[str] = None,
			log:jk_logging.AbstractLogger,
		) -> str:

		if args:
			raise Exception("Invoke this method with named arguments only!")

		assert isinstance(srcDirPath, str)
		assert isinstance(destTarFilePath, str)
		if filesAndDirsToInclude is not None:
			assert isinstance(filesAndDirsToInclude, (tuple,list))
			for fn in filesAndDirsToInclude:
				assert isinstance(fn, str)
				assert fn
		chModValue = jk_utils.ChModValue.createN(chModValue)
		chModValueI = None if chModValue is None else chModValue.toInt()
		assert isinstance(log, jk_logging.AbstractLogger)

		# ----

		with log.descend("Packing " + repr(srcDirPath) + " ...") as log2:
			srcDirPath = os.path.abspath(srcDirPath)
			assert os.path.isdir(srcDirPath)
			destTarFilePath = os.path.abspath(destTarFilePath)

			if filesAndDirsToInclude is None:
				filesAndDirsToInclude = [ x.name for x in os.scandir(srcDirPath) ]

			if not os.path.isfile(Packer1._TAR_PATH):
				raise Exception("'tar' not found!")

			tarArgs = [
				"-cf", destTarFilePath
			] + filesAndDirsToInclude

			log2.notice("Invoking /bin/tar ...")
			_oldmask = os.umask(0o777 ^ chModValueI) if chModValueI is not None else None
			try:
				cmdResult = jk_simpleexec.invokeCmd2(
					cmdPath=Packer1._TAR_PATH,
					cmdArgs=tarArgs,
					workingDirectory=srcDirPath,
				)
			finally:
				if _oldmask is not None:
					os.umask(_oldmask)
					os.chmod(destTarFilePath, chModValueI)	# required as tar will not set the execute bit

			if cmdResult.returnCode != 0:
				cmdResult.dump(printFunc=log2.error)
				raise Exception("Failed to run 'tar'!")

		# ----

		return destTarFilePath
	#

	@staticmethod
	@jk_utils.deprecated
	def compressFile(
			filePath:str,
			compression:str,
			bDeleteOriginal:bool,
			terminationFlag:typing.Union[jk_utils.TerminationFlag,None],
			log:jk_logging.AbstractLogger
		) -> str:

		assert isinstance(filePath, str)
		assert isinstance(compression, str)
		assert isinstance(bDeleteOriginal, bool)
		assert isinstance(log, jk_logging.AbstractLogger)

		# ----

		with log.descend("Compressing " + repr(filePath) + " ...") as log2:
			filePath = os.path.abspath(filePath)
			assert os.path.isfile(filePath)

			name, ext, m = Packer1._getCompressionParams(compression)

			log.notice("Packing with " + name + " ...")

			orgFileSize = os.path.getsize(filePath)

			toFilePath = filePath + ext

			# TODO: check if target file already exists

			m(filePath, toFilePath, None, terminationFlag)

			resultFileSize = os.path.getsize(toFilePath)
			compressionFactor = round(100 * resultFileSize / orgFileSize, 2)
			log.notice("Compression factor: {}%".format(compressionFactor))

			if bDeleteOriginal:
				if os.path.isfile(filePath):
					os.unlink(filePath)
			else:
				if not os.path.isfile(filePath):
					raise Exception("Implementation error!")

			return toFilePath
	#

	#
	# Compress the specified file.
	#
	# @param	str filePath						(required) The path of the file to compress.
	# @param	str toFilePath						(optional) The path of the file to write the compressed data to.
	#												If <c>None</c> a new file path is created with suitable exension based on the
	#												compression type.
	# @param	str compression						(required) The compression. Valid values are: "gz", "gzip", "bz2", "bzip2", "xz"
	# @param	bool bDeleteOriginal				(required) If <c>True</c> the source file will be deleted after successfull compression.
	# @param	int|str|ChModValue chModValue		(optional) If specified this change-mode value will be used to set the permission of
	#												the created file.
	# @param	TerminationFlag terminationFlag		(optional) A termination flag for graceful asynchroneous termination.
	# @param	AbstractLogger log					(required) A logger to write log information to
	#
	@staticmethod
	def compressFile2(
			filePath:str,
			toFilePath:typing.Union[str,None],
			compression:str,
			bDeleteOriginal:bool,
			chModValue:typing.Union[int,str,jk_utils.ChModValue,None],
			terminationFlag:typing.Union[jk_utils.TerminationFlag,None],
			log:jk_logging.AbstractLogger,
		) -> SpoolInfo:
		return Packer1.compressFile3(
			filePath=filePath,
			toFilePath=toFilePath,
			compression=compression,
			bDeleteOriginal=bDeleteOriginal,
			chModValue=chModValue,
			terminationFlag=terminationFlag,
			log=log,
		)
	#

	#
	# Compress the specified file.
	#
	# @param	str filePath						(required) The path of the file to compress.
	# @param	str toFilePath						(optional) The path of the file to write the compressed data to.
	#												If <c>None</c> a new file path is created with suitable exension based on the
	#												compression type.
	# @param	str compression						(required) The compression. Valid values are: "gz", "gzip", "bz2", "bzip2", "xz"
	# @param	bool bDeleteOriginal				(required) If <c>True</c> the source file will be deleted after successfull compression.
	# @param	int|str|ChModValue chModValue		(optional) If specified this change-mode value will be used to set the permission of
	#												the created file.
	# @param	TerminationFlag terminationFlag		(optional) A termination flag for graceful asynchroneous termination.
	# @param	AbstractLogger log					(required) A logger to write log information to
	#
	@staticmethod
	def compressFile3(
			*args,
			filePath:str,
			toFilePath:str = None,
			compression:str,
			bDeleteOriginal:bool = False,
			chModValue:typing.Union[int,str,jk_utils.ChModValue,None] = None,
			terminationFlag:jk_utils.TerminationFlag = None,
			log:jk_logging.AbstractLogger,
		) -> SpoolInfo:

		if args:
			raise Exception("Invoke this method with named arguments only!")

		assert isinstance(filePath, str)
		if toFilePath is not None:
			assert isinstance(toFilePath, str)
		assert isinstance(compression, str)
		assert isinstance(bDeleteOriginal, bool)
		chModValue = jk_utils.ChModValue.createN(chModValue)
		chModValueI = None if chModValue is None else chModValue.toInt()
		assert isinstance(log, jk_logging.AbstractLogger)

		# ----

		with log.descend("Compressing " + repr(filePath) + " ...") as log2:
			filePath = os.path.abspath(filePath)
			assert os.path.isfile(filePath)

			compressionName, compressionFileExt, m = Packer1._getCompressionParams(compression)

			log.notice("Packing with " + compressionName + " ...")

			orgFileSize = os.path.getsize(filePath)

			if toFilePath is None:
				toFilePath = filePath + compressionFileExt

			# TODO: check if target file already exists

			m(filePath, toFilePath, chModValueI, terminationFlag)

			resultFileSize = os.path.getsize(toFilePath)

			if bDeleteOriginal:
				if os.path.isfile(filePath):
					os.unlink(filePath)
			else:
				if not os.path.isfile(filePath):
					raise Exception("Implementation error!")

			return SpoolInfo(filePath, toFilePath, compressionName, compressionFileExt, orgFileSize, resultFileSize)
	#

#






















