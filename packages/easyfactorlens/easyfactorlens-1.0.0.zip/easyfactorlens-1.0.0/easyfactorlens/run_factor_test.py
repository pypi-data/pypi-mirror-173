import pandas as pd
import numpy as np
import statsmodels.api as sm
import warnings
from tqdm import tqdm
import utilities
from loguru import logger

warnings.filterwarnings('ignore')

logger_path = './factor_logs.log'
factor_info = "测试因子"
data_file = r'C:\Users\Administrator\Desktop\ricequant_local_alphalens\data'

logger.add(logger_path, rotation="500MB", encoding="utf-8", enqueue=True,
           compression='zip',
           retention="365 days")  # 日志配置

logger.info('-------------------------------------------------')
logger.info(f'因子简介：{factor_info}')


# MAD:中位数去极值
def filter_extreme_MAD(series, n):
    logger.info('因子去极值')
    median = series.median()
    new_median = ((series - median).abs()).median()
    return series.clip(median - n * new_median, median + n * new_median)


def winsorize_std(series, n=3):
    mean, std = series.mean(), series.std()
    return series.clip(mean - std * n, mean + std * n)


def winsorize_percentile(series, left=0.025, right=0.975):
    lv, rv = np.percentile(series, [left * 100, right * 100])
    return series.clip(lv, rv)

def run():
    # 读取因子表，进行表调整
    logger.info('读取因子表，进行表调整')
    df_cfoa_whole = pd.read_csv(f'{data_file}/df_cfoa_whole.csv', index_col='date')

    # 读取过滤表
    logger.info('读取ST过滤表')
    st_filter = pd.read_csv(f'{data_file}/st_filter.csv', index_col='date')
    logger.info('读取停牌过滤表')
    get_suspended_filter = pd.read_csv(f'{data_file}/get_suspended_filter.csv', index_col='date')
    logger.info('读取涨跌停过滤表')
    get_limit_up_down_filter = pd.read_csv(f'{data_file}/get_limit_up_down_filter.csv', index_col='date')
    logger.info('读取新股过滤表')
    new_stock_filter = pd.read_csv(f'{data_file}/new_stock_filter.csv', index_col='date')

    # 使用mask过滤
    logger.info('过滤数据')
    df_cfoa_whole_filter = df_cfoa_whole.mask(st_filter).mask(get_suspended_filter).mask(get_limit_up_down_filter).mask(
        new_stock_filter).dropna(axis=1, how='all')
    df_cfoa_whole = df_cfoa_whole.unstack().reset_index()
    df_cfoa_whole.columns = ['order_book_id', 'date', 'factor_value']
    df_cfoa_whole = df_cfoa_whole[['date', 'order_book_id', 'factor_value']]

    # 读取市值表
    logger.info('读取市值表')
    df_market_cap_whole = pd.read_csv(f'{data_file}/df_market_cap_whole.csv')

    # 读取行业信息表
    logger.info('读取行业信息表')
    industry_df = pd.read_csv(f'{data_file}/industry_df.csv')
    industry = pd.read_csv(f'{data_file}/industry_result.csv')

    # 表拼接
    logger.info('进行表拼接')
    cfoa_industy_market = pd.concat([df_cfoa_whole, industry, df_market_cap_whole, industry_df], axis=1)
    cfoa_industy_market = cfoa_industy_market.loc[:, ~cfoa_industy_market.columns.duplicated()]
    cfoa_industy_market.sort_values(['date', 'order_book_id'], inplace=True)
    cfoa_industy_market.dropna(inplace=True)
    cfoa_industy_market = cfoa_industy_market.reset_index(drop=True)

    # 动态中性化、拼接
    logger.info('进行行业市值中性化')
    cfoa_result = pd.DataFrame()
    datetime_period = sorted(list(set(cfoa_industy_market['date'].values)))
    for i in tqdm(datetime_period, desc='动态行业市值中性化进度：'):
        cfoa_day = cfoa_industy_market[cfoa_industy_market['date'] == i]  # 截面数据做回归
        x = cfoa_day.iloc[:, 4:]  # 市值/行业
        y = cfoa_day.iloc[:, 2]  # 因子值
        cfoa_day_result = pd.DataFrame(sm.OLS(y.astype(float), x.astype(float), hasconst=False, missing='drop').fit().resid)
        cfoa_result = pd.concat([cfoa_result, cfoa_day_result], axis=0)
    cfoa_industy_market['factor_value'] = cfoa_result
    cfoa_industy_market = cfoa_industy_market[['date', 'order_book_id', 'factor_value', 'industry']]

    # 读取价格表并处理
    logger.info('读取、处理股票收盘价表')
    close_price = pd.read_csv(f'{data_file}/close_price.csv')
    close_price = pd.merge(left=cfoa_industy_market, right=close_price, left_on=['date', 'order_book_id'],
                           right_on=['date', 'order_book_id'], how='left')

    close_price = close_price[['date', 'order_book_id', 'close']]
    close_price['date'] = pd.to_datetime(close_price['date'])
    close_price = close_price.set_index(['date', 'order_book_id']).unstack('order_book_id')
    close_price = close_price.tz_localize('UTC')
    close_price.columns = close_price.columns.get_level_values(1)

    # 读取因子表并处理
    logger.info('读取、处理因子整合表')
    cfoa_industy_market = cfoa_industy_market[['date', 'order_book_id', 'factor_value', 'industry']]
    cfoa_industy_market['date'] = pd.to_datetime(cfoa_industy_market['date'])
    cfoa_industy_market = cfoa_industy_market.set_index(['date']).tz_localize('UTC')
    cfoa_industy_market = cfoa_industy_market.reset_index().set_index(['date', 'order_book_id'])

    # 跑alphalens
    logger.info('跑alphalens')
    alphalens_data = utilities.utils.get_clean_factor_and_forward_returns(factor=cfoa_industy_market['factor_value'],
                                                                                    prices=close_price,
                                                                                    groupby=cfoa_industy_market['industry'],
                                                                                    max_loss=0.35)
    utilities.tears.create_full_tear_sheet(alphalens_data, by_group=True)
if __name__ == '__main__':
    run()