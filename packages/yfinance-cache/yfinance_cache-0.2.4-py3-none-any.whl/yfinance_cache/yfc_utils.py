from enum import Enum
import os
from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo
import re
import numpy as np

class OperatingSystem(Enum):
	Windows = 1
	Linux = 2
	OSX = 3


def GetOperatingSystem():
	if os.name == "nt":
		return OperatingSystem.Windows
	elif os.name == "posix":
		return OperatingSystem.Linux
	else:
		raise Exception("Unknwon os.name = '{0}'".format(os.name))


def GetUserCacheDirpath():
	_os = GetOperatingSystem()
	if _os == OperatingSystem.Windows:
		dp = os.getenv("APPDATA")
		raise Exception("Not tested. Does this make sense as cache dir in Windows? - {0}".format(dp))
	elif _os == OperatingSystem.Linux:
		dp = os.path.join(os.getenv("HOME"), ".cache")
	else:
		raise Exception("Not implemented: cache dirpath under OS '{0}'".format(_os))
	return dp


def JsonEncodeValue(value):
	if isinstance(value, date):
		return value.isoformat()
	elif isinstance(value, timedelta):
		e = "timedelta-{0}".format(value.total_seconds())
		return e
	raise TypeError()


def JsonDecodeDict(value):
	for k in value.keys():
		v = value[k]
		if isinstance(v,str) and v.startswith("timedelta-"):
			try:
				sfx = '-'.join(v.split('-')[1:])
				sfxf = float(sfx)
				value[k] = timedelta(seconds=sfxf)
			except:
				pass
		else:
			## TODO: add suffix "date-" or "datetime-". Will need to upgrade existing cache
			decoded = False
			try:
				value[k] = date.fromisoformat(v)
				decoded = True
			except:
				pass
			if not decoded:
				try:
					value[k] = datetime.fromisoformat(v)
					decoded = True
				except:
					pass

	return value


def GetSigFigs(n):
	if n == 0:
		return 0
	n_str = str(n).replace('.', '')
	m = re.match( r'0*[1-9](\d*[1-9])?', n_str)
	sf = len(m.group())

	return sf


def GetMagnitude(n):
	m = 0
	if n >= 1.0:
		while n >= 1.0:
			n *= 0.1
			m += 1
	else:
		while n < 1.0:
			n *= 10.0
			m -= 1

	return m


def CalculateRounding(n, sigfigs):
	if GetSigFigs(round(n)) >= sigfigs:
		return 0
	elif round(n,0)==n:
		return 0
	else:
		return sigfigs - GetSigFigs(round(n))


def GetCSF0(df):
	if not "Stock Splits" in df:
		raise Exception("DataFrame does not contain column 'Stock Splits")
	if df.shape[0] == 0:
		raise Exception("DataFrame is empty")

	ss = df["Stock Splits"].copy()
	ss[ss==0.0] = 1.0

	if "CSF" in df.columns:
		csf = df["CSF"]
	else:
		ss_rcp = 1.0/ss
		csf = ss_rcp.sort_index(ascending=False).cumprod().sort_index(ascending=True).shift(-1, fill_value=1.0)
	csf0 = csf[0]

	ss0 = ss.iloc[0]
	if ss0 != 1.0:
		csf0 *= 1.0/ss0

	return csf0


def GetCDF0(df):
	if not "CDF" in df:
		raise Exception("DataFrame does not contain column 'CDF")
	if df.shape[0] == 0:
		raise Exception("DataFrame is empty")

	cdf = df["CDF"][0]
	if cdf != 1.0:
		# Yahoo's dividend adjustment has tiny variation (~1e-6), 
		# so use mean to minimise accuracy loss of adjusted->deadjust->adjust
		i = np.argmax(df["Dividends"]!=0.0) -1
		if i < 0:
			print("df:")
			print(df)
			raise Exception("i shouldn't < 0")
		cdf_mean = df["CDF"].iloc[0:i].mean()
		if abs(cdf_mean-cdf)/cdf > 0.0001:
			raise Exception("Mean CDF={} is sig. different to CDF[0]={}".format(cdf_mean, cdf))
		cdf = cdf_mean

	div0 = df["Dividends"][0]
	if div0 != 0.0:
		close = df["Close"][1]
		cdf *= (close-div0)/close

	return cdf

