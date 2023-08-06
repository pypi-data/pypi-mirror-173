from pprint import pprint

from datetime import datetime, date, time, timedelta
from dateutil.relativedelta import relativedelta
from zoneinfo import ZoneInfo

import sys ; sys.path.insert(0, "/home/gonzo/ReposForks/exchange_calendars.dev")
import exchange_calendars as xcal

import pandas as pd
import numpy as np

from . import yfc_dat as yfcd
from . import yfc_cache_manager as yfcm


def TypeCheckStr(var, varName):
	if not isinstance(var, str):
		raise Exception("'{}' must be str not {}".format(varName, type(var)))
def TypeCheckBool(var, varName):
	if not isinstance(var, bool):
		raise Exception("'{}' must be bool not {}".format(varName, type(var)))
def TypeCheckDateEasy(var, varName):
	if not (isinstance(var, date) or isinstance(var, datetime)):
		raise Exception("'{}' must be date not {}".format(varName, type(var)))
	if isinstance(var, datetime):
		if var.tzinfo is None:
			raise Exception("'{}' if datetime must be timezone-aware".format(varName))
		elif not isinstance(var.tzinfo, ZoneInfo):
			raise Exception("'{}' tzinfo must be ZoneInfo".format(varName))
def TypeCheckDateStrict(var, varName):
	if isinstance(var, pd.Timestamp):
		# While Pandas missing support for 'zoneinfo' must deny
		raise Exception("'{}' must be date not {}".format(varName, type(var)))
	if not (isinstance(var, date) and not isinstance(var, datetime)):
		raise Exception("'{}' must be date not {}".format(varName, type(var)))
def TypeCheckDatetime(var, varName):
	if not isinstance(var, datetime):
		raise Exception("'{}' must be datetime not {}".format(varName, type(var)))
	if var.tzinfo is None:
		raise Exception("'{}' if datetime must be timezone-aware".format(varName))
	elif not isinstance(var.tzinfo, ZoneInfo):
		raise Exception("'{}' tzinfo must be ZoneInfo".format(varName))
def TypeCheckTimedelta(var, varName):
	if not isinstance(var, timedelta):
		raise Exception("'{}' must be timedelta not {}".format(varName, type(var)))
def TypeCheckInterval(var, varName):
	if not isinstance(var, yfcd.Interval):
		raise Exception("'{}' must be yfcd.Interval not {}".format(varName, type(var)))
def TypeCheckIntervalDt(dt, interval, varName, strict=True):
	if interval in [yfcd.Interval.Days1, yfcd.Interval.Week]:
		if strict:
			TypeCheckDateStrict(dt, varName)
		else:
			TypeCheckDateEasy(dt, varName)
	else:
		TypeCheckDatetime(dt, varName)
def TypeCheckPeriod(var, varName):
	if not isinstance(var, yfcd.Period):
		raise Exception("'{}' must be yfcd.Period not {}".format(varName, type(var)))
def TypeCheckNpArray(var, varName):
	if not isinstance(var, np.ndarray):
		raise Exception("'{}' must be numpy array not {}".format(varName, type(var)))

exchangeTzCache = {}
def GetExchangeTzName(exchange):
	TypeCheckStr(exchange, "exchange")

	if not exchange in exchangeTzCache:
		tz = yfcm.ReadCacheDatum("exchange-"+exchange, "tz")
		if tz is None:
			raise Exception("Do not know timezone for exchange '{}'".format(exchange))
		exchangeTzCache[exchange] = tz
	else:
		tz = exchangeTzCache[exchange]
	return tz
def SetExchangeTzName(exchange, tz):
	TypeCheckStr(exchange, "exchange")
	TypeCheckStr(tz, "tz")
	
	tzc = yfcm.ReadCacheDatum("exchange-"+exchange, "tz")
	if not tzc is None:
		if tzc != tz:
			## Different names but maybe same tz
			tzc_zi = ZoneInfo(tzc)
			tz_zi = ZoneInfo(tz)
			dt = datetime.now()
			if tz_zi.utcoffset(dt) != tzc_zi.utcoffset(dt):
				print("tz_zi = {} ({})".format(tz_zi, type(tz_zi)))
				print("tzc_zi = {} ({})".format(tzc_zi, type(tzc_zi)))
				raise Exception("For exchange '{}', new tz {} != cached tz {}".format(exchange, tz, tzc))
	else:
		exchangeTzCache[exchange] = tz
		yfcm.StoreCacheDatum("exchange-"+exchange, "tz", tz)


def GetExchangeDataDelay(exchange):
	TypeCheckStr(exchange, "exchange")

	d = yfcm.ReadCacheDatum("exchange-"+exchange, "yf_lag")
	if d is None:
		d = yfcd.exchangeToYfLag[exchange]
	return d


def GetCalendar(exchange):
	cal = xcal.get_calendar(yfcd.exchangeToXcalExchange[exchange], start=str(yfcd.yf_min_year), cache=True)

	df = cal.schedule
	tz = ZoneInfo(GetExchangeTzName(exchange))
	df["open"] = df["open"].dt.tz_convert(tz)
	df["close"] = df["close"].dt.tz_convert(tz)

	if (exchange in yfcd.exchangesWithAuction) and ("auction" not in df.columns):
		df["auction"] = df["close"] + yfcd.exchangeAuctionDelay[exchange]

	return cal

def ExchangeOpenOnDay(exchange, d):
	TypeCheckStr(exchange, "exchange")
	TypeCheckDateStrict(d, "d")

	if not exchange in yfcd.exchangeToXcalExchange:
		raise Exception("Need to add mapping of exchange {} to xcal".format(exchange))
	cal = GetCalendar(exchange)

	return d.isoformat() in cal.schedule.index


def GetExchangeSchedule(exchange, start_d, end_d):
	TypeCheckStr(exchange, "exchange")
	TypeCheckDateStrict(start_d, "start_d")
	TypeCheckDateStrict(end_d, "end_d")

	if start_d >= end_d:
		raise Exception("start_d={} must < end_d={}".format(start_d, end_d))

	if not exchange in yfcd.exchangeToXcalExchange:
		raise Exception("Need to add mapping of exchange {} to xcal".format(exchange))
	cal = GetCalendar(exchange)

	sched = None
	## loc[] is inclusive, but end_d should be treated as exclusive:
	sched = cal.schedule[start_d:end_d-timedelta(days=1)]
	if (sched is None) or sched.shape[0] == 0:
		return None

	cols = ["open","close"]
	if "auction" in sched.columns:
		cols.append("auction")
	df = sched[cols].copy()
	df = df.rename(columns={"open":"market_open","close":"market_close"})
	return df


def GetExchangeWeekSchedule(exchange, start, end, weeklyUseYahooDef=True):
	TypeCheckStr(exchange, "exchange")
	if start >= end:
		raise Exception("start={} must be < end={}".format(start, end))
	TypeCheckDateEasy(start, "start")
	TypeCheckDateEasy(end, "end")

	tz = ZoneInfo(GetExchangeTzName(exchange))
	td_1d = timedelta(days=1)
	if not isinstance(start, datetime):
		start_dt = datetime.combine(start, time(0), tz)
		start_d = start
	else:
		start_dt = start
		start_d = start.astimezone(tz).date()
	if not isinstance(end, datetime):
		end_dt = datetime.combine(end, time(0), tz)
		end_d = end
	else:
		end_dt = end
		end_d = end.astimezone(tz).date() +td_1d

	debug = False

	week_starts_sunday = (exchange in ["TLV"]) and (not weeklyUseYahooDef)
	if debug:
		print("- week_starts_sunday =", week_starts_sunday)

	if not exchange in yfcd.exchangeToXcalExchange:
		raise Exception("Need to add mapping of exchange {} to xcal".format(exchange))
	cal = GetCalendar(exchange)

	open_dts = cal.schedule.loc[start_d.isoformat():(end_d-td_1d).isoformat()]["open"]
	if len(open_dts) == 0:
		return None
	open_dts = pd.DatetimeIndex(open_dts).tz_convert(tz).tz_localize(None)

	if debug:
		print("open_dts:")
		print(open_dts)

	if week_starts_sunday:
		weeks = open_dts.groupby(open_dts.to_period("W-SAT"))
	else:
		weeks = open_dts.groupby(open_dts.to_period("W"))
	weeks_keys = sorted(list(weeks.keys()))

	if debug:
		print("weeks:")
		# pprint(weeks)
		for k in weeks:
			print("- {}->{}".format(k.start_time, k.end_time))
			print(weeks[k].date)
		print("")

	if weeklyUseYahooDef:
		td_7d = timedelta(days=7)
		week_ranges = [(w.start_time.date(), w.start_time.date()+td_7d) for w in weeks.keys()]
	else:
		week_ranges = [(w[0].date(), w[-1].date()+td_1d) for w in weeks.values()]

	if debug:
		print("week_ranges:")
		pprint(week_ranges)

	first_week_cutoff = False
	last_week_cutoff = False
	if weeklyUseYahooDef:
		k = weeks_keys[0]
		prev_sesh = cal.previous_session(weeks[k][0].date())
		if debug:
			print("- prev_sesh:", prev_sesh)
		first_week_cutoff = prev_sesh >= k.start_time

		k = weeks_keys[-1]
		next_sesh = cal.next_session(weeks[k][-1].date())
		if debug:
			print("- next_sesh:", next_sesh)
		last_week_cutoff = next_sesh <= k.end_time

	else:
		# Add one day to start and end. If returns more open days, then means
		# above date range cuts off weeks.
		open_dts_wrap = cal.schedule.loc[(start_d-td_1d).isoformat():end_d.isoformat()]["open"]
		open_dts_wrap = pd.DatetimeIndex(open_dts_wrap).tz_convert(tz).tz_localize(None)
		if week_starts_sunday:
			weeks2 = open_dts_wrap.groupby(open_dts_wrap.to_period("W-SAT"))
		else:
			weeks2 = open_dts_wrap.groupby(open_dts_wrap.to_period("W"))

		if debug:
			print("open_dts_wrap:")
			print(open_dts_wrap)

		if debug:
			print("weeks2:")
			# pprint(weeks2)
			for k in weeks2:
				print("- ",k)
				print(weeks2[k].date)

		k0 = sorted(list(weeks.keys()))[0]
		m0 = sorted(list(weeks2.keys()))[0]
		if k0 == m0:
			if weeks2[m0][0] < weeks[k0][0]:
				first_week_cutoff = True

		kn1 = sorted(list(weeks.keys()))[-1]
		mn1 = sorted(list(weeks2.keys()))[-1]
		if kn1 == mn1:
			if weeks2[mn1][-1] > weeks[kn1][-1]:
				last_week_cutoff = True

	if debug:
		print("first_week_cutoff:", first_week_cutoff)
		print("last_week_cutoff:", last_week_cutoff)

	week_ranges = sorted(week_ranges, key=lambda x: x[0])
	if last_week_cutoff:
		del week_ranges[-1]
	if first_week_cutoff:
		del week_ranges[0]
	if len(week_ranges) == 0:
		week_ranges = None

	return week_ranges


def GetExchangeScheduleIntervals(exchange, interval, start, end, weeklyUseYahooDef=True):
	TypeCheckStr(exchange, "exchange")
	if start >= end:
		raise Exception("start={} must be < end={}".format(start, end))
	TypeCheckDateEasy(start, "start")
	TypeCheckDateEasy(end, "end")

	debug = False
	# debug = True

	if debug:
		print("GetExchangeScheduleIntervals(start={}, end={}, weeklyUseYahooDef={})".format(start, end, weeklyUseYahooDef))

	week_starts_sunday = (exchange in ["TLV"]) and (not weeklyUseYahooDef)
	if debug:
		print("- week_starts_sunday =", week_starts_sunday)

	if not exchange in yfcd.exchangeToXcalExchange:
		raise Exception("Need to add mapping of exchange {} to xcal".format(exchange))
	cal = GetCalendar(exchange)

	tz = ZoneInfo(GetExchangeTzName(exchange))
	td_1d = timedelta(days=1)
	if not isinstance(start, datetime):
		start_dt = datetime.combine(start, time(0), tz)
		start_d = start
	else:
		start_dt = start
		start_d = start.astimezone(tz).date()
	if not isinstance(end, datetime):
		end_dt = datetime.combine(end, time(0), tz)
		end_d = end
	else:
		end_dt = end
		end_d = end.astimezone(tz).date() +td_1d

	if debug:
		print("- start_d={}, end_d={}".format(start_d, end_d))

	intervals = None
	istr = yfcd.intervalToString[interval]
	td = yfcd.intervalToTimedelta[interval]
	if istr.endswith('h') or istr.endswith('m'):
		if td > timedelta(minutes=30):
			align = '30m'
		else:
			align = istr
		ti = cal.trading_index(start_d.isoformat(), end_d.isoformat(), period=istr, intervals=True, force_close=True, align=align)
		if len(ti) == 0:
			return None
		# Transfer IntervalIndex to DataFrame so can modify
		intervals_df = pd.DataFrame(data={"interval_open":ti.left.tz_convert(tz), "interval_close":ti.right.tz_convert(tz)})
		if "auction" in cal.schedule.columns:
			sched = cal.schedule.loc[start_d:end_d]
			sched.index=sched.index.date

			market_opens = intervals_df.groupby(intervals_df["interval_open"].dt.date).min()["interval_open"]
			market_opens.name = "day_open"
			market_opens.index.name = "day"
			if istr.endswith('h'):
				res = istr.replace('h','H')
			else:
				res = istr.replace('m','T')
			auctions_df = sched[["auction"]].copy()
			auctions_df = auctions_df.join(market_opens)
			offset = auctions_df["day_open"] - auctions_df["day_open"].dt.floor(res)
			auctions_df = auctions_df.drop("day_open", axis=1)
			auctions_df["auction_open"] = (auctions_df["auction"]-offset).dt.floor(res)+offset
			auctions_df["auction_close"] = auctions_df["auction"] + yfcd.exchangeAuctionDuration[exchange]
			auctions_df = auctions_df.drop("auction", axis=1)

			# Compare auction intervals against last trading interval
			intervals_df_last = intervals_df.groupby(intervals_df["interval_open"].dt.date).max()
			intervals_df_ex_last = intervals_df[~intervals_df["interval_open"].isin(intervals_df_last["interval_open"])]
			intervals_df_last.index = intervals_df_last["interval_open"].dt.date
			auctions_df = auctions_df.join(intervals_df_last)
			# - if auction surrounded by trading, discard auction
			f_surround = (auctions_df["auction_open"]  >= auctions_df["interval_open"]) & \
						 (auctions_df["auction_close"] <= auctions_df["interval_close"])
			if f_surround.any():
				# print("dropping surrounded auction")
				auctions_df.loc[f_surround, ["auction_open", "auction_close"]] = pd.NaT
			# - if last trading interval surrounded by auction, then replace by auction
			f_surround = (auctions_df["interval_open"]  >= auctions_df["auction_open"]) & \
						 (auctions_df["interval_close"] <= auctions_df["auction_close"])
			if f_surround.any():
				# print("dropping surrounded trading")
				auctions_df.loc[f_surround, ["interval_open", "interval_close"]] = pd.NaT
			# - no duplicates, no overlaps
			f_duplicate = (auctions_df["auction_open"]  == auctions_df["interval_open"]) & \
						  (auctions_df["auction_close"] == auctions_df["interval_close"])
			if f_duplicate.any():
				print("")
				print(auctions_df[f_duplicate])
				raise Exception("Auction intervals are duplicates of normal trading intervals")
			f_overlap = (auctions_df["auction_open"] >= auctions_df["interval_open"]) & \
						(auctions_df["auction_open"]  < auctions_df["interval_close"])
			if f_overlap.any():
				# First, if total duration is <= interval length, then combine
				d = auctions_df["auction_close"] - auctions_df["interval_open"]
				f = d<=td
				if f.any():
					# Combine
					auctions_df.loc[f,"auction_open"] = auctions_df.loc[f,"interval_open"]
					auctions_df.loc[f,["interval_open", "interval_close"]] = pd.NaT
					f_overlap = (auctions_df["auction_open"] >= auctions_df["interval_open"]) & \
								(auctions_df["auction_open"]  < auctions_df["interval_close"])
				if f_overlap.any():
					print("")
					print(auctions_df[f_overlap])
					raise Exception("Auction intervals are overlapping normal trading intervals")
			# - combine
			auctions_df = auctions_df.reset_index(drop=True)
			intervals_df_last = auctions_df.loc[~auctions_df["interval_open"].isna(),["interval_open","interval_close"]]
			auctions_df = auctions_df.loc[~auctions_df["auction_open"].isna(),["auction_open","auction_close"]].rename(columns={"auction_open":"interval_open","auction_close":"interval_close"})
			intervals_df = pd.concat([intervals_df_ex_last, intervals_df_last, auctions_df], sort=True).sort_values(by="interval_open").reset_index(drop=True)

		intervals_df = intervals_df[(intervals_df["interval_open"]>=start_dt) & (intervals_df["interval_close"]<=end_dt)]
		if intervals_df.shape[0] == 0:
			raise Exception("WARNING: No intervals generated for date range {} -> {}".format(start, end))
			return None
		intervals = pd.IntervalIndex.from_arrays(intervals_df["interval_open"], intervals_df["interval_close"], closed="left")

	elif interval == yfcd.Interval.Days1:
		s = cal.schedule.loc[start_d.isoformat():(end_d-timedelta(days=1)).isoformat()]
		s = s[(s["open"]>=start_dt) & (s["close"]<=end_dt)]
		if s.shape[0] == 0:
			return None
		open_days = np.array([dt.to_pydatetime().astimezone(tz).date() for dt in s["open"]])
		intervals = yfcd.DateIntervalIndex.from_arrays(open_days, open_days+td_1d, closed="left")

	elif interval == yfcd.Interval.Week:
		week_ranges = GetExchangeWeekSchedule(exchange, start, end, weeklyUseYahooDef)

		intervals = yfcd.DateIntervalIndex.from_arrays([w[0] for w in week_ranges], [w[1] for w in week_ranges], closed="left")

	else:
		raise Exception("Need to implement for interval={}".format(interval))

	if debug:
		print("GetExchangeScheduleIntervals() returning")

	return intervals


def IsTimestampInActiveSession(exchange, ts):
	TypeCheckStr(exchange, "exchange")
	TypeCheckDatetime(ts, "ts")

	cal = GetCalendar(exchange)
	try:
		s = cal.schedule.loc[ts.date().isoformat()]
	except:
		return False

	o=s["open"] ; c=s["close"]
	if "auction" in cal.schedule.columns:
		a = s["auction"]
		if a != pd.NaT:
			c = max(c, s["auction"]+yfcd.exchangeAuctionDuration[exchange])

	return o<=ts and ts<c


def GetTimestampCurrentSession(exchange, ts):
	TypeCheckStr(exchange, "exchange")
	TypeCheckDatetime(ts, "ts")

	cal = GetCalendar(exchange)
	try:
		s = cal.schedule.loc[ts.date().isoformat()]
	except:
		return None
	o=s["open"] ; c=s["close"]
	if "auction" in cal.schedule.columns:
		a = s["auction"]
		if a != pd.NaT:
			c = max(c, s["auction"]+yfcd.exchangeAuctionDuration[exchange])

	if o<=ts and ts<c:
		return {"market_open":o, "market_close":c}
	else:
		return None


def GetTimestampMostRecentSession(exchange, ts):
	TypeCheckStr(exchange, "exchange")
	TypeCheckDatetime(ts, "ts")

	## If 'ts' is currently in an active session then that is most recent

	s = GetTimestampCurrentSession(exchange, ts)
	if not s is None:
		return s
	sched = GetExchangeSchedule(exchange, ts.date()-timedelta(days=6), ts.date()+timedelta(days=1))
	if "auction" in sched.columns:
		f = ~(sched["auction"].isna())
		if f.any():
			if f.all():
				sched["market_close"] = np.maximum(sched["market_close"], sched["auction"]+yfcd.exchangeAuctionDuration[exchange])
			else:
				sched.loc[f,"market_close"] = np.maximum(sched.loc[f,"market_close"], sched.loc[f,"auction"]+yfcd.exchangeAuctionDuration[exchange])
	for i in range(sched.shape[0]-1, -1, -1):
		if sched["market_open"][i] <= ts:
			tz = ZoneInfo(GetExchangeTzName(exchange))
			return {"market_open":sched["market_open"][i].to_pydatetime().astimezone(tz), "market_close":sched["market_close"][i].to_pydatetime().astimezone(tz)}
	raise Exception("Failed to find most recent '{0}' session for ts = {1}".format(exchange, ts))


def GetTimestampNextSession(exchange, ts):
	TypeCheckStr(exchange, "exchange")
	TypeCheckDatetime(ts, "ts")

	sched = GetExchangeSchedule(exchange, ts.date(), ts.date()+timedelta(days=7))
	if "auction" in sched.columns:
		f = ~(sched["auction"].isna())
		if f.any():
			if f.all():
				sched["market_close"] = np.maximum(sched["market_close"], sched["auction"]+yfcd.exchangeAuctionDuration[exchange])
			else:
				sched.loc[f,"market_close"] = np.maximum(sched.loc[f,"market_close"], sched.loc[f,"auction"]+yfcd.exchangeAuctionDuration[exchange])
	for i in range(sched.shape[0]):
		if ts < sched["market_open"][i]:
			tz = ZoneInfo(GetExchangeTzName(exchange))
			return {"market_open":sched["market_open"][i].to_pydatetime().astimezone(tz), "market_close":sched["market_close"][i].to_pydatetime().astimezone(tz)}
	raise Exception("Failed to find next '{0}' session for ts = {1}".format(exchange, ts))


def GetTimestampCurrentInterval(exchange, ts, interval, weeklyUseYahooDef=True):
	TypeCheckStr(exchange, "exchange")
	TypeCheckIntervalDt(ts, interval, "ts", strict=False)
	TypeCheckInterval(interval, "interval")
	TypeCheckBool(weeklyUseYahooDef, "weeklyUseYahooDef")

	# For day and week intervals, the time component is ignored (set to 0).

	debug = False
	# debug = True

	if debug:
		print("GetTimestampCurrentInterval(ts={}, interval={}, weeklyUseYahooDef={})".format(ts, interval, weeklyUseYahooDef))

	week_starts_sunday = (exchange in ["TLV"]) and (not weeklyUseYahooDef)

	i = None

	tz = ZoneInfo(GetExchangeTzName(exchange))
	if interval == yfcd.Interval.Week:
		# Treat week intervals as special case, contiguous from first weekday open to last weekday open. 
		# Not necessarily Monday->Friday because of public holidays.
		# Unless 'weeklyUseYahooDef' is true, which means range from Monday to Friday.
		## UPDATE: Extending range to Sunday midnight aka next Monday
		if isinstance(ts,datetime):
			ts_day = ts.astimezone(tz).date()
		else:
			ts_day = ts

		if week_starts_sunday:
			if ts_day.weekday()==6:
				# Already at start of week
				weekStart = ts_day
			else:
				weekStart = ts_day - timedelta(days=ts_day.weekday()+1)
		else:
			weekStart = ts_day - timedelta(days=ts_day.weekday())

		if weeklyUseYahooDef:
			weekEnd = weekStart + timedelta(days=7)
		else:
			weekEnd = weekStart + timedelta(days=5)
		if debug:
			print("- weekStart = {}".format(weekStart))
			print("- weekEnd = {}".format(weekEnd))
		if not weeklyUseYahooDef:
			weekSched = GetExchangeSchedule(exchange, weekStart, weekEnd)
			weekStart = weekSched["market_open"][0].date()
			weekEnd = weekSched["market_close"][-1].date()+timedelta(days=1)
		intervalStart = weekStart
		intervalEnd = weekEnd
		if debug:
			print("- intervalStart = {}".format(intervalStart))
			print("- intervalEnd = {}".format(intervalEnd))
		if ts_day >= intervalStart:
			if (ts_day < intervalEnd):
				i = {"interval_open":intervalStart, "interval_close":intervalEnd}

	elif interval == yfcd.Interval.Days1:
		if isinstance(ts, datetime):
			ts_day = ts.astimezone(tz).date()
		else:
			ts_day = ts
		if debug:
			print("- ts_day: {}".format(ts_day))
		if ExchangeOpenOnDay(exchange, ts_day):
			if debug:
				print("- exchange open")
			daySched = GetExchangeSchedule(exchange, ts_day, ts_day+timedelta(days=1))
			i = {"interval_open":daySched["market_open"][0].date(), "interval_close":daySched["market_close"][0].date()+timedelta(days=1)}
		else:
			if debug:
				print("- exchange closed")

	else:
		if IsTimestampInActiveSession(exchange, ts) or IsTimestampInActiveSession(exchange, ts+timedelta(minutes=30)):
			ts = ts.astimezone(tz)
			td = yfcd.intervalToTimedelta[interval]
			if exchange in yfcd.exchangesWithAuction:
				td = max(td, timedelta(minutes=15))
			intervals = GetExchangeScheduleIntervals(exchange, interval, ts-td, ts+timedelta(minutes=30)+td)
			idx = intervals.get_indexer([ts])
			f = idx!=-1
			if f.any():
				i0 = intervals[idx[f]][0]
				i = {"interval_open":i0.left.to_pydatetime(), "interval_close":i0.right.to_pydatetime()}

	if debug:
		print("GetTimestampCurrentInterval() returning: {}".format(i))

	return i

def GetTimestampCurrentInterval_batch(exchange, ts, interval, weeklyUseYahooDef=True):
	TypeCheckStr(exchange, "exchange")
	if isinstance(ts,list):
		ts = np.array(ts)
	TypeCheckNpArray(ts, "ts")
	TypeCheckIntervalDt(ts[0], interval, "ts", strict=False)
	TypeCheckInterval(interval, "interval")
	TypeCheckBool(weeklyUseYahooDef, "weeklyUseYahooDef")

	# For day and week intervals, the time component is ignored (set to 0).

	debug = False
	# debug = True

	if debug:
		print("GetTimestampCurrentInterval_batch(ts[0]={}, interval={}, weeklyUseYahooDef={})".format(ts[0], interval, weeklyUseYahooDef))

	n = len(ts)
	tz = ZoneInfo(GetExchangeTzName(exchange))
	intervals = [None]*n

	td_1d = timedelta(days=1)
	tz = ZoneInfo(GetExchangeTzName(exchange))
	tz_utc = ZoneInfo("UTC")
	ts_is_datetimes = isinstance(ts[0],datetime)
	if ts_is_datetimes:
		ts_day = [t.astimezone(tz).date() for t in ts]
		# ts_day = list(map(lambda x: x.astimezone(tz).date(), ts))
	else:
		ts_day = ts

	if interval == yfcd.Interval.Week:
		# Treat week intervals as special case, contiguous from first weekday open to last weekday open. 
		# Not necessarily Monday->Friday because of public holidays.
		# Unless 'weeklyUseYahooDef' is true, which means range from Monday to Friday.
		#
		t0 = ts_day[0]  ; t0 -= timedelta(days=t0.weekday())+timedelta(days=7)
		tl = ts_day[-1] ; tl += timedelta(days=6-tl.weekday())+timedelta(days=7)
		if debug:
			print("t0={} ; tl={}".format(t0, tl))
		sched = GetExchangeSchedule(exchange, t0, tl)

		if weeklyUseYahooDef:
			# Monday -> next Monday regardless of exchange schedule
			weekSchedStart = [d-timedelta(days=d.weekday()) for d in ts_day]
			weekSchedEnd = [ws+timedelta(days=7) for ws in weekSchedStart]
		else:
			week_sched = GetExchangeScheduleIntervals(exchange, interval, t0, tl, weeklyUseYahooDef)
			weekSchedStart = np.full(n, None)
			weekSchedEnd = np.full(n, None)
			left = pd.to_datetime(week_sched.left).tz_localize(tz)
			right = pd.to_datetime(week_sched.right).tz_localize(tz)

			week_sched = pd.IntervalIndex.from_arrays(left, right, closed="left")
			idx = week_sched.get_indexer(ts)
			f = idx!=-1
			if f.any():
				weekSchedStart[f] = week_sched.left[idx[f]].date
				weekSchedEnd[f] = week_sched.right[idx[f]].date

		intervals = pd.DataFrame(data={"interval_open":weekSchedStart, "interval_close":weekSchedEnd}, index=ts)

	elif interval == yfcd.Interval.Days1:
		t0 = ts_day[0]
		tl = ts_day[len(ts_day)-1]
		sched = GetExchangeSchedule(exchange, t0, tl+timedelta(days=1))
		#
		ts_day = pd.to_datetime(ts_day)
		ts_day_df = pd.DataFrame(index=ts_day)
		intervals = pd.merge(ts_day_df, sched, how="left", left_index=True, right_index=True)
		intervals = intervals.rename(columns={"market_open":"interval_open", "market_close":"interval_close"})
		intervals["interval_open"] = intervals["interval_open"].dt.date
		intervals["interval_close"] = intervals["interval_close"].dt.date +td_1d

	else:
		td = yfcd.intervalToTimedelta[interval]
		if exchange == "ASX":
			td = max(td, timedelta(minutes=15))
		cal = GetCalendar(exchange)
		t0 = ts[0]
		tl = ts[len(ts)-1]
		tis = GetExchangeScheduleIntervals(exchange, interval, t0-td, tl+td)
		if debug:
			print("- trading index:", type(tis))
			for ti in tis:
				print(ti)
		tz_tis = tis[0].left.tzinfo
		if ts[0].tzinfo != tz_tis:
			ts = [t.astimezone(tz_tis) for t in ts]
		idx = tis.get_indexer(ts)
		f = idx!=-1
		#
		intervals = pd.DataFrame(index=ts)
		intervals["interval_open"] = pd.NaT
		intervals["interval_close"] = pd.NaT
		if f.any():
			intervals.loc[intervals.index[f], "interval_open"] = tis.left[idx[f]].tz_convert(tz)
			intervals.loc[intervals.index[f], "interval_close"] = tis.right[idx[f]].tz_convert(tz)

	if debug:
		print("GetTimestampCurrentInterval_batch() returning")

	return intervals

def GetTimestampNextInterval(exchange, ts, interval, weeklyUseYahooDef=True):
	TypeCheckStr(exchange, "exchange")
	TypeCheckIntervalDt(ts, interval, "ts", strict=False)
	TypeCheckInterval(interval, "interval")
	TypeCheckBool(weeklyUseYahooDef, "weeklyUseYahooDef")

	debug = False
	# debug = True

	if debug:
		print("GetTimestampNextInterval(exchange={}, ts={}, interval={})".format(exchange, ts, interval))

	td_1d = timedelta(days=1)
	tz = ZoneInfo(GetExchangeTzName(exchange))
	ts_d = ts.astimezone(tz).date()

	if interval in [yfcd.Interval.Days1, yfcd.Interval.Week]:
		if interval == yfcd.Interval.Days1:
			next_day = ts_d + td_1d
			s = GetTimestampNextSession(exchange, datetime.combine(next_day, time(0), tz))
			interval_open  = s["market_open"].date()
			interval_close = interval_open+td_1d
		else:
			week_sched = GetExchangeWeekSchedule(exchange, ts_d, ts_d+14*td_1d, weeklyUseYahooDef)
			if ts_d >= week_sched[0][0]:
				week_sched = week_sched[1:]
			interval_open = week_sched[0][0]
			interval_close = week_sched[0][1]
		return {"interval_open":interval_open, "interval_close":interval_close}

	interval_td = yfcd.intervalToTimedelta[interval]
	c = GetTimestampCurrentInterval(exchange, ts, interval)
	if debug:
		if c is None:
			print("- currentInterval = None")
		else:
			print("- currentInterval = {} -> {}".format(c["interval_open"], c["interval_close"]))

	next_interval_close = None
	td = yfcd.intervalToTimedelta[interval]
	if (c is None) or not IsTimestampInActiveSession(exchange, c["interval_close"]):
		next_sesh = GetTimestampNextSession(exchange, ts)
		if debug:
			print("- next_sesh = {}".format(next_sesh))
		if exchange=="TLV":
			istr = yfcd.intervalToString[interval]
			if td > timedelta(minutes=30):
				align = '30m'
			else:
				align = istr
			d = next_sesh["market_open"].date()
			ti = GetCalendar(exchange).trading_index(d.isoformat(), (d+td_1d).isoformat(), period=istr, intervals=True, force_close=True, align=align)
			next_interval_start = ti.left[0]
		else:
			next_interval_start = next_sesh["market_open"]
	else:
		if exchange in yfcd.exchangesWithAuction:
			day_sched = GetExchangeSchedule(exchange, ts_d, ts_d+td_1d).iloc[0]
			if c["interval_close"] < day_sched["market_close"]:
				# Next is normal trading
				next_interval_start = c["interval_close"]
			else:
				# Next is auction
				if td <= timedelta(minutes=10):
					next_interval_start = day_sched["auction"]
				else:
					next_interval_start = day_sched["market_close"]
				next_interval_close = day_sched["auction"] + yfcd.exchangeAuctionDuration[exchange]
		else:
			next_interval_start = c["interval_close"]

	if next_interval_close is None:
		next_interval_close = next_interval_start + interval_td

	if debug:
		print("GetTimestampNextInterval() returning")
	return {"interval_open":next_interval_start, "interval_close":next_interval_close}


def CalcIntervalLastDataDt(exchange, intervalStart, interval, yf_lag=None):
	# When does Yahoo stop receiving data for this interval?
	TypeCheckStr(exchange, "exchange")
	TypeCheckIntervalDt(intervalStart, interval, "intervalStart", strict=False)
	TypeCheckInterval(interval, "interval")

	debug = False
	# debug = True

	if debug:
		print("CalcIntervalLastDataDt(intervalStart={}, interval={})".format(intervalStart, interval))

	if not yf_lag is None:
		TypeCheckTimedelta(yf_lag, "yf_lag")
	else:
		yf_lag = GetExchangeDataDelay(exchange)

	tz = ZoneInfo(GetExchangeTzName(exchange))

	irange = GetTimestampCurrentInterval(exchange, intervalStart, interval)
	if irange is None:
		raise Exception("Failed to map {} to interval".format(intervalStart))
	if debug:
		print("- irange:")
		pprint(irange)

	if isinstance(irange["interval_open"],datetime):
		intervalSched = GetExchangeSchedule(exchange, irange["interval_open"].astimezone(tz).date(), irange["interval_close"].astimezone(tz).date()+timedelta(days=1))
	else:
		intervalSched = GetExchangeSchedule(exchange, irange["interval_open"], irange["interval_close"])
	if debug:
		print("- intervalSched:")
		pprint(intervalSched)

	intervalEnd = irange["interval_close"]
	if isinstance(intervalEnd, datetime):
		intervalEnd_dt = intervalEnd
	else:
		intervalEnd_dt = datetime.combine(intervalEnd, time(0), ZoneInfo(GetExchangeTzName(exchange)))

	lastDataDt = min(intervalEnd_dt, intervalSched["market_close"][-1]) +yf_lag

	# For some exchanges, Yahoo has trades that occurred soon afer official market close, e.g. Johannesburg:
	if exchange in ["JNB"]:
		late_data_allowance = timedelta(minutes=15)
	else:
		late_data_allowance = timedelta(0)

	if (interval in [yfcd.Interval.Days1, yfcd.Interval.Week]) or (intervalEnd_dt==intervalSched["market_close"][-1]):
		## Is daily/weekly interval or last interval of day:
		lastDataDt += late_data_allowance

	if debug:
		print("CalcIntervalLastDataDt() returning {}".format(lastDataDt))

	return lastDataDt

def CalcIntervalLastDataDt_batch(exchange, intervalStart, interval, yf_lag=None):
	# When does Yahoo stop receiving data for this interval?
	TypeCheckStr(exchange, "exchange")
	if isinstance(intervalStart,list):
		intervalStart = np.array(intervalStart)
	TypeCheckNpArray(intervalStart, "intervalStart")
	TypeCheckIntervalDt(intervalStart[0], interval, "intervalStart", strict=False)
	TypeCheckInterval(interval, "interval")

	debug = False
	# debug = True

	if debug:
		print("CalcIntervalLastDataDt_batch(interval={}, yf_lag={})".format(interval, yf_lag))

	if not yf_lag is None:
		TypeCheckTimedelta(yf_lag, "yf_lag")
	else:
		yf_lag = GetExchangeDataDelay(exchange)

	n = len(intervalStart)
	tz = ZoneInfo(GetExchangeTzName(exchange))

	intervals = GetTimestampCurrentInterval_batch(exchange, intervalStart, interval)
	if isinstance(intervals["interval_open"].iloc[0], datetime):
		iopens = intervals["interval_open"]
		icloses = intervals["interval_close"]
	else:
		iopens = intervals["interval_open"].values
		icloses = intervals["interval_close"].values
	if debug:
		print("- intervals:")
		print(intervals)

	marketCloses = np.array([None]*n)
	iopen0 = iopens[0]
	iclosel = icloses[len(icloses)-1]
	if isinstance(iopen0, datetime):
		if isinstance(iopen0, pd.Timestamp):
			iopen0 = iopen0.to_pydatetime()
			iclosel = iclosel.to_pydatetime()
		sched = GetExchangeSchedule(exchange, iopen0.astimezone(tz).date(), iclosel.astimezone(tz).date()+timedelta(days=1))
	else:
		sched = GetExchangeSchedule(exchange, iopen0, iclosel+timedelta(days=1))
	sched["day"] = sched["market_open"].dt.date
	is_dt = isinstance(iopens[0], datetime)
	if is_dt:
		iopen0 = iopens[0]
		if isinstance(iopen0, pd.Timestamp):
			iclose_days = [i.astimezone(tz).date() for i in icloses]
		else:
			iclose_days = [i.astimezone(tz).date() for i in icloses]
	else:
		iclose_days = [i-timedelta(days=1) for i in icloses]
	icloses_df = pd.DataFrame(data={"iopen":iopens, "iclose":icloses, "day":iclose_days})
	icloses_df2 = icloses_df.merge(sched[["day","market_close"]], on="day", how="left")
	f_na = icloses_df2["market_close"].isna()
	if f_na.any():
		if interval in [yfcd.Interval.Week, yfcd.Interval.Months1, yfcd.Interval.Months3]:
			# Search back a little
			attempts = 4 # Worst-case = 9/11, have to search back from Friday to Monday to find actual open day
			while f_na.any() and attempts > 0:
				icloses_df2 = icloses_df2.drop("market_close",axis=1)
				icloses_df2.loc[f_na,"day"] -= timedelta(days=1)
				icloses_df2 = icloses_df2.merge(sched[["day","market_close"]], on="day", how="left")
				attempts -= 1
				f_na = icloses_df2["market_close"].isna()
		if f_na.any():
			raise Exception("Lost data in merge")
	icloses_df = icloses_df2
	marketCloses = icloses_df["market_close"].dt.to_pydatetime()
	if debug:
		print("- icloses_df:")
		print(icloses_df)

	if (marketCloses==None).any():
		raise Exception("Failed to map some intervals to schedule")

	dc0 = icloses[0]
	if isinstance(dc0, datetime):
		intervalEnd_dt = [x.to_pydatetime().astimezone(tz) for x in icloses]
	else:
		intervalEnd_dt = [datetime.combine(dc, time(0), tz) for dc in icloses]

	lastDataDt = np.minimum(intervalEnd_dt, marketCloses) +yf_lag

	# For some exchanges, Yahoo has trades that occurred soon afer official market close, e.g. Johannesburg:
	if exchange in ["JNB"]:
		late_data_allowance = timedelta(minutes=15)
		if interval in [yfcd.Interval.Days1, yfcd.Interval.Week]:
			lastDataDt += late_data_allowance
		else:
			lastDataDt[intervalEnd_dt == marketCloses] += late_data_allowance

	if debug:
		print("CalcIntervalLastDataDt_batch() returning")

	return lastDataDt


def IsPriceDatapointExpired(intervalStart, fetch_dt, max_age, exchange, interval, triggerExpiryOnClose=True, yf_lag=None, dt_now=None):
	TypeCheckIntervalDt(intervalStart, interval, "intervalStart", strict=False)
	TypeCheckDatetime(fetch_dt, "fetch_dt")
	TypeCheckTimedelta(max_age, "max_age")
	TypeCheckStr(exchange, "exchange")
	TypeCheckInterval(interval, "interval")
	TypeCheckBool(triggerExpiryOnClose, "triggerExpiryOnClose")

	debug = False
	# debug = True

	if debug:
		print("") ; print("")
		print("IsPriceDatapointExpired(intervalStart={}, fetch_dt={}, max_age={}, triggerExpiryOnClose={}, dt_now={})".format(intervalStart, fetch_dt, max_age, triggerExpiryOnClose, dt_now))

	if not dt_now is None:
		TypeCheckDatetime(dt_now, "dt_now")
	else:
		dt_now = datetime.utcnow().replace(tzinfo=ZoneInfo("UTC"))

	if not yf_lag is None:
		TypeCheckTimedelta(yf_lag, "yf_lag")
	else:
		yf_lag = GetExchangeDataDelay(exchange)
	if debug:
		print("yf_lag = {}".format(yf_lag))

	irange = GetTimestampCurrentInterval(exchange, intervalStart, interval)
	if debug:
		print("- irange = {}".format(irange))

	if irange is None:
		print("market open? = {}".format(IsTimestampInActiveSession(exchange, intervalStart)))
		raise Exception("Failed to map '{}'' to '{}' interval range".format(intervalStart, interval))

	intervalEnd = irange["interval_close"]
	if isinstance(intervalEnd, datetime):
		intervalEnd_d = intervalEnd.date()
	else:
		intervalEnd_d = intervalEnd
	if debug:
		print("- intervalEnd_d = {0}".format(intervalEnd_d))

	lastDataDt = CalcIntervalLastDataDt(exchange, intervalStart, interval, yf_lag)
	if debug:
		print("- lastDataDt = {}".format(lastDataDt))

	# Decide if was fetched after last Yahoo update
	if interval in [yfcd.Interval.Days1, yfcd.Interval.Week]:
		if fetch_dt >= lastDataDt:
			## interval already closed before fetch, nothing to do.
			if debug:
				print("- fetch_dt > lastDataDt so return FALSE")
			return False
	else:
		interval_already_closed = fetch_dt > lastDataDt
		if interval_already_closed:
			## interval already closed before fetch, nothing to do.
			if debug:
				print("- fetch_dt > lastDataDt so return FALSE")
			return False

	expire_dt = fetch_dt+max_age
	if debug:
		print("- expire_dt = {0}".format(expire_dt))
	if expire_dt < lastDataDt and expire_dt <= dt_now:
		if debug:
			print("- expire_dt < lastDataDt and expire_dt <= dt_now so return TRUE")
		return True

	if triggerExpiryOnClose:
		if debug:
			print("- checking if triggerExpiryOnClose ...")
			print("- - fetch_dt            = {}".format(fetch_dt))
			print("- - lastDataDt = {}".format(lastDataDt))
			print("- - dt_now              = {}".format(dt_now))
		if (fetch_dt < lastDataDt) and (lastDataDt <= dt_now):
			## Even though fetched data hasn't fully aged, the candle has since closed so treat as expired
			if debug:
				print("- triggerExpiryOnClose and interval closed so return TRUE")
			return True
		if interval in [yfcd.Interval.Days1, yfcd.Interval.Week]:
			## If last fetch was anytime within interval, even post-market, 
			## and dt_now is next day (or later) then trigger
			if fetch_dt.date() <= intervalEnd_d and dt_now.date() > intervalEnd_d:
				if debug:
					print("- triggerExpiryOnClose and interval midnight passed since fetch so return TRUE")
				return True

	if debug:
		print("- reached end of function, returning FALSE")
	return False


def IdentifyMissingIntervals(exchange, start, end, interval, knownIntervalStarts, weeklyUseYahooDef=True):
	TypeCheckStr(exchange, "exchange")
	TypeCheckDateEasy(start, "start")
	TypeCheckDateEasy(end, "end")
	if start >= end:
		raise Exception("start={} must be < end={}".format(start, end))
	if not knownIntervalStarts is None:
		if not isinstance(knownIntervalStarts, list) and not isinstance(knownIntervalStarts, np.ndarray):
			raise Exception("'knownIntervalStarts' must be list or numpy array not {0}".format(type(knownIntervalStarts)))
		if interval in [yfcd.Interval.Days1, yfcd.Interval.Week]:
			## Must be date
			TypeCheckDateStrict(knownIntervalStarts[0], "knownIntervalStarts")
		else:
			## Must be datetime
			TypeCheckDatetime(knownIntervalStarts[0], "knownIntervalStarts")
			if knownIntervalStarts[0].tzinfo is None:
				raise Exception("'knownIntervalStarts' dates must be timezone-aware")

	debug = False
	# debug = True

	if debug:
		print("IdentifyMissingIntervals()")
		print("- start={}, end={}".format(start, end))
		print("- knownIntervalStarts:")
		pprint(knownIntervalStarts)

	intervals = GetExchangeScheduleIntervals(exchange, interval, start, end, weeklyUseYahooDef)
	if (intervals is None) or (intervals.shape[0]==0):
		raise yfcd.NoIntervalsInRangeException(interval, start, end)
	if debug:
		print("- intervals:")
		pprint(intervals)

	if not knownIntervalStarts is None:
		intervalStarts = intervals.left
		if isinstance(intervalStarts[0], (datetime, pd.Timestamp)):
			intervalStarts = [i.timestamp() for i in intervalStarts.to_pydatetime()]
			knownIntervalStarts = [x.timestamp() for x in knownIntervalStarts]
		if debug:
			print("- intervalStarts:")
			print(intervalStarts)

		intervalStarts = np.array(intervalStarts)
		knownIntervalStarts = np.array(knownIntervalStarts)
		if intervalStarts.dtype.hasobject or knownIntervalStarts.dtype.hasobject:
			## Apparently not optimised in numpy, faster to DIY
			## https://github.com/numpy/numpy/issues/14997#issuecomment-560516888
			knownIntervalStarts_set = set(knownIntervalStarts)
			f_missing = ~np.array([elem in knownIntervalStarts_set for elem in intervalStarts])
		else:
			f_missing = np.isin(intervalStarts, knownIntervalStarts, invert=True)
	else:
		f_missing = np.full(intervals.shape[0], True)

	intervals_missing_df = pd.DataFrame(data={"open":intervals[f_missing].left,"close":intervals[f_missing].right}, index=np.where(f_missing)[0])
	if debug:
		print("- intervals_missing_df:")
		print(intervals_missing_df)

	if debug:
		print("IdentifyMissingIntervals() returning")
	return intervals_missing_df

def IdentifyMissingIntervalRanges(exchange, start, end, interval, knownIntervalStarts, weeklyUseYahooDef=True, minDistanceThreshold=5):
	TypeCheckStr(exchange, "exchange")
	TypeCheckDateEasy(start, "start")
	TypeCheckDateEasy(end, "end")
	if start >= end:
		raise Exception("start={} must be < end={}".format(start, end))
	if not knownIntervalStarts is None:
		if not isinstance(knownIntervalStarts, list) and not isinstance(knownIntervalStarts, np.ndarray):
			raise Exception("'knownIntervalStarts' must be list or numpy array not {0}".format(type(knownIntervalStarts)))
		if interval in [yfcd.Interval.Days1, yfcd.Interval.Week]:
			## Must be date or datetime
			TypeCheckDateEasy(knownIntervalStarts[0], "knownIntervalStarts")
			if isinstance(knownIntervalStarts[0],datetime) and knownIntervalStarts[0].tzinfo is None:
				raise Exception("'knownIntervalStarts' datetimes must be timezone-aware")
		else:
			## Must be datetime
			TypeCheckDatetime(knownIntervalStarts[0], "knownIntervalStarts")
			if knownIntervalStarts[0].tzinfo is None:
				raise Exception("'knownIntervalStarts' dates must be timezone-aware")

	debug = False
	# debug = True

	if debug:
		print("IdentifyMissingIntervalRanges()")
		print("- start={}, end={}".format(start, end))
		print("- knownIntervalStarts:")
		pprint(knownIntervalStarts)

	intervals = GetExchangeScheduleIntervals(exchange, interval, start, end, weeklyUseYahooDef)
	if intervals is None or intervals.shape[0]==0:
		raise yfcd.NoIntervalsInRangeException(interval, start, end)
	if debug:
		print("- intervals:")
		for i in intervals:
			print(i)

	intervals_missing_df = IdentifyMissingIntervals(exchange, start, end, interval, knownIntervalStarts, weeklyUseYahooDef)
	if debug:
		print("- intervals_missing_df:")
		pprint(intervals_missing_df)

	f_missing=np.full(intervals.shape[0], False) ; f_missing[intervals_missing_df.index]=True

	## Merge together near ranges if the distance between is below threshold.
	## This is to reduce web requests
	i_true = np.where(f_missing)[0]
	for i in range(len(i_true)-1):
		i0 = i_true[i]
		i1 = i_true[i+1]
		if i1-i0 <= minDistanceThreshold+1:
			## Mark all intervals between as missing, thus merging together 
			## the pair of missing ranges
			f_missing[i0+1:i1] = True
	if debug:
		print("- f_missing:")
		pprint(f_missing)

	## Scan for contiguous sets of missing intervals:
	ranges = []
	i_true = np.where(f_missing)[0]
	if len(i_true) > 0:
		start=None ; end=None
		for i in range(len(f_missing)):
			v = f_missing[i]
			if v:
				if start is None:
					start=i ; end=i
				else:
					if i == (end+1):
						end = i
					else:
						r = (intervals[start].left, intervals[end].right)
						ranges.append(r)
						start = i ; end = i

			if i == (len(f_missing)-1):
				r = (intervals[start].left, intervals[end].right)
				ranges.append(r)

	if debug:
		print("- ranges:")
		pprint(ranges)

	if debug:
		print("IdentifyMissingIntervalRanges() returning")

	if len(ranges) == 0:
		return None
	return ranges


def ConvertToDatetime(dt, tz=None):
	## Convert numpy.datetime64 -> pandas.Timestamp -> python datetime
	if isinstance(dt, np.datetime64):
		dt = pd.Timestamp(dt)
	if isinstance(dt, pd.Timestamp):
		dt = dt.to_pydatetime()
	if not tz is None:
		if dt.tzinfo is None:
			dt = dt.replace(tzinfo=tz)
		else:
			dt = dt.astimezone(tz)
	return dt


def DtSubtractPeriod(dt, period):
	TypeCheckDateEasy(dt, "dt")
	TypeCheckPeriod(period, "period")

	if period==yfcd.Period.Ytd:
		if isinstance(dt, datetime):
			return datetime(dt.year, 1, 1, tzinfo=dt.tzinfo)
		else:
			return date(dt.year, 1, 1)

	if period==yfcd.Period.Days1:
		rd = relativedelta(days=1)
	elif period==yfcd.Period.Days5:
		rd = relativedelta(days=5)
	elif period==yfcd.Period.Week:
		rd = relativedelta(days=7)
	elif period==yfcd.Period.Months1:
		rd = relativedelta(months=1)
	elif period==yfcd.Period.Months3:
		rd = relativedelta(months=3)
	elif period==yfcd.Period.Months6:
		rd = relativedelta(months=6)
	elif period==yfcd.Period.Years1:
		rd = relativedelta(years=1)
	elif period==yfcd.Period.Years2:
		rd = relativedelta(years=2)
	elif period==yfcd.Period.Years5:
		rd = relativedelta(years=5)
	elif period==yfcd.Period.Years10:
		rd = relativedelta(years=10)
	else:
		raise Exception("Unknown period value '{}'".format(period))

	return dt - rd


def GetSystemTz():
	dt = datetime.utcnow().astimezone()

	# tz = dt.tzinfo
	tzn = dt.tzname()
	if tzn == "BST":
		## Confirmed that ZoneInfo figures out DST
		tzn = "GB"
	tz = ZoneInfo(tzn)
	return tz

