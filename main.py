import pandas as pd

df = pd.read_csv("p1_data.csv")
df_c = df[df['variant'] == 'Control']
df_v = df[df['variant'] == 'Variant']

N_c = len(df_c)  # Number of experiments in control group
N_v = len(df_v)  # Number of experiments in variant group

P_c = df_c['purchaser'].sum()  # Number of success in control group
P_v = df_v['purchaser'].sum()  # Number of success in variant group

print("Purchase/view rate in control group:", P_c / N_c)
print("Purchase/view rate in variant group:", P_v / N_v)

# Analyse for primary metric:

# 1. purchase/view rate

# Distribution: Binomial. Confidence interval: 5%.
# Customer who complete a purchase will be a success, otherwise it will be a failure.
# H0: The purchase/view rate has no change. H1: The purchase/view rate is improved.

from scipy.stats import binomtest

k = P_v
n = N_v
p = P_c / N_c

res = binomtest(k, n, p)
print('binomial test p value = ', res.pvalue)
if res.pvalue < 0.05:
    print('The null hypothesis is rejected. '
          'At confidence interval of 5%, we can say the purchase/view rate is improved.')
else:
    print('The null hypothesis is accepted. '
          'At confidence interval of 5%, we can say the purchase/view rate stays the same.')

# Analyse Pooled Standard Error

df_pool = (P_c + P_v) / (N_c + N_v)
df_SE_pool = (df_pool * (1 - df_pool) * (1 / N_c + 1 / N_v)) ** (1 / 2)

# Take d to be difference of results from two experiments
# H0 : There is a difference between two results. H1: There is no difference.
# Use normal distribution with mean = 0 and standard error = df_SE_pool

d = P_v / N_v - P_c / N_c
print("Difference between two results: ", d)
print("1.96 * SE of Pooled Standard Error:", 1.96 * df_SE_pool)
if d < 1.96 * df_SE_pool:
    print('The null hypothesis for pooled standard error is accepted.'
          'The increase in purchase/view rate is not significant considering the sample size.')
else:
    print('The null hypothesis for pooled standard error is rejected.'
          'The increase in purchase/view rate is significant considering the sample size.')


# 2. Total booking value

# Distribution: Normal. Confidence interval：5%. Standard normal Z value at 5% = 1.645
# Need to compare the mean of total booking value for each customer. Proceed with T test.

from scipy.stats import ttest_ind

df_ct = df_c['total_booking_value_USD']
df_vt = df_v['total_booking_value_USD']

print("Total sales mean for control: ", df_ct.mean())
print("Total sales mean for variant: ", df_vt.mean())

# H0: mean does not change. H1: mean decreases.

print('std value for control:', df_ct.std())
print('std value for variant:', df_vt.std())

ttest, pval = ttest_ind(df_ct, df_vt)
print("t test p value: ", pval)

if res.pvalue < 0.05:
    print('The null hypothesis is rejected. '
          'At confidence interval of nearly 0%, we can say the average for total sales is decreased.')
else:
    print('The null hypothesis is accepted. '
          'At confidence interval of nearly 0%, we can say the average for total sales stays the same.')

# Secondary metric :

# 1.Total booking value / length of stay

df['result'] = df['total_booking_value_USD']/df['bkg_room_nights']
df = df.fillna(0)
df = df[df['result']!= 0]
df_control = df.loc[df['variant'] == 'Control', 'result']
df_variant = df.loc[df['variant'] == 'Variant', 'result']

print("Mean total booking value / length of stay for control: ", df_control.mean())
print("Mean total booking value / length of stay for variant: ", df_variant.mean())


# H0: total booking value / length of stay for control stays unchanged.
# H1: total booking value / length of stay for control decreased.

# Use T test

ttest, pval = ttest_ind(df_variant, df_control)
print("t test p value: ", pval)

if res.pvalue < 0.05:
    print('The null hypothesis is rejected. '
          'At confidence interval of nearly 0%, we can say the average for total sales / length of stay is decreased.')
else:
    print('The null hypothesis is accepted. '
          'At confidence interval of nearly 0%, we can say the average for total sales / length of stay is increased.')

# Length of stay

df = pd.read_csv("p1_data.csv")

df_cl = df_c.loc[df_c['length_of_stay'] == 'Long Break more than 5', 'length_of_stay']
df_vl = df_v.loc[df_v['length_of_stay'] == 'Long Break more than 5', 'length_of_stay']
df_cs = df_c.loc[df_c['length_of_stay'] == 'Short Break less than 4', 'length_of_stay']
df_vs = df_v.loc[df_v['length_of_stay'] == 'Short Break less than 4', 'length_of_stay']
print('% of customers stay longer for control:', len(df_cl) / N_c, 'For variant:', len(df_vl) / N_v)

# Distribution: Binomial. Confidence interval: 5%
# H0：% of customers stay longer does not change. H1: It decreases.

k = len(df_vl)
n = N_v
p = len(df_cl) / N_c

res = binomtest(k, n, p)
print('binomial test p value = ', 1 - res.pvalue)
if 1 - res.pvalue < 0.05:
    print('The null hypothesis is rejected. '
          'At confidence interval of 5%, we can say the % of customers stay longer is improved.')
else:
    print('The null hypothesis is accepted. '
          'At confidence interval of 5%, we can say the % of customers stay longer stays unchanged.')


# Is there a correlation between staying longer and higher purchase/view rate?

df_l = df[df["length_of_stay"] == 'Long Break more than 5']
df_s = df[df["length_of_stay"] == 'Short Break less than 4']

# Distribution: Binomial. Confidence interval: 5%
# H0: No correlation(stays the same), H1: The longer stay time, the higher purchase/view rate.

print("The purchase/view rate for customers who stay longer: ", df_l['purchaser'].sum() / len(df_l), 'For who stay shorter:', df_s['purchaser'].sum() / len(df_s))

k = df_l['purchaser'].sum()
n = len(df_l)
p = df_s['purchaser'].sum() / len(df_s)

res = binomtest(k, n, p)
print('binomial test p value = ', res.pvalue)
if res.pvalue < 0.05:
    print('The null hypothesis is rejected. '
          'At confidence interval of 5%, we can say the % of customers stay longer is improved.')
else:
    print('The null hypothesis is accepted. '
          'At confidence interval of 5%, we can say the % of customers stay longer stays unchanged.')

print("Overall, because of the negative feedbacks from hypothesis testing of two primary metrics and two secondary "
      "metrics, I will not recommend the change on website. ")

# Dimension:

# Purchase/view:

df = pd.read_csv("p1_data.csv")

df_c = df[df['variant'] == 'Control']
df_v = df[df['variant'] == 'Variant']

# Platform type:

df_cd = df_c[df_c['platform_type'] == 'Desktop']
df_vd = df_v[df_v['platform_type'] == 'Desktop']
df_ct = df_c[df_c['platform_type'] == 'Tablet']
df_vt = df_v[df_v['platform_type'] == 'Tablet']

print('Purchase/view rate for control group who uses Desktop: ', df_cd['purchaser'].sum()/len(df_cd), "For variant group:", df_vd['purchaser'].sum()/len(df_vd))
print('Purchase/view rate for control group who uses Tablet: ', df_ct['purchaser'].sum()/len(df_ct), "For variant group:", df_vt['purchaser'].sum()/len(df_vt))

# new or return

df_cd = df_c[df_c['new_visitor_ind'] == 'new']
df_vd = df_v[df_v['new_visitor_ind'] == 'new']
df_ct = df_c[df_c['new_visitor_ind'] == 'return']
df_vt = df_v[df_v['new_visitor_ind'] == 'return']

print('Purchase/view rate for control group who is new: ', df_cd['purchaser'].sum()/len(df_cd), "For variant group:", df_vd['purchaser'].sum()/len(df_vd))
print('Purchase/view rate for control group who returns: ', df_ct['purchaser'].sum()/len(df_ct), "For variant group:", df_vt['purchaser'].sum()/len(df_vt))

# browser type

df_cd = df_c[df_c['brwsr_typ_name'] == 'Microsoft']
df_vd = df_v[df_v['brwsr_typ_name'] == 'Microsoft']
df_ct = df_c[df_c['brwsr_typ_name'] == 'Google']
df_vt = df_v[df_v['brwsr_typ_name'] == 'Google']
df_ca = df_c[df_c['brwsr_typ_name'] == 'Safari']
df_va = df_v[df_v['brwsr_typ_name'] == 'Safari']
df_cb = df_c[df_c['brwsr_typ_name'] == 'Unknown']
df_vb = df_v[df_v['brwsr_typ_name'] == 'Unknown']

print('Purchase/view rate for control group who uses Microsoft ', df_cd['purchaser'].sum()/len(df_cd), "For variant group:", df_vd['purchaser'].sum()/len(df_vd))
print('Purchase/view rate for control group who uses Google ', df_ct['purchaser'].sum()/len(df_ct), "For variant group:", df_vt['purchaser'].sum()/len(df_vt))
print('Purchase/view rate for control group who uses Safari ', df_ca['purchaser'].sum()/len(df_ca), "For variant group:", df_va['purchaser'].sum()/len(df_va))
print('Purchase/view rate for control group who comes from Unknown: ', df_cb['purchaser'].sum()/len(df_cb), "For variant group:", df_vb['purchaser'].sum()/len(df_vb))

# Partnership

df_cd = df_c[df_c['property_super_regn_name'] == 'AMER']
df_vd = df_v[df_v['property_super_regn_name'] == 'AMER']
df_ct = df_c[df_c['property_super_regn_name'] == 'EMEA']
df_vt = df_v[df_v['property_super_regn_name'] == 'EMEA']
df_ca = df_c[df_c['property_super_regn_name'] == 'APAC']
df_va = df_v[df_v['property_super_regn_name'] == 'APAC']
df_cb = df_c[df_c['property_super_regn_name'] == 'Accor']
df_vb = df_v[df_v['property_super_regn_name'] == 'Accor']
df_cc = df_c[df_c['property_super_regn_name'] == 'LATAM']
df_vc = df_v[df_v['property_super_regn_name'] == 'LATAM']


print('Purchase/view rate for control group who uses AMER ', df_cd['purchaser'].sum()/len(df_cd), "For variant group:", df_vd['purchaser'].sum()/len(df_vd))
print('Purchase/view rate for control group who uses EMEA ', df_ct['purchaser'].sum()/len(df_ct), "For variant group:", df_vt['purchaser'].sum()/len(df_vt))
print('Purchase/view rate for control group who uses APAC ', df_ca['purchaser'].sum()/len(df_ca), "For variant group:", df_va['purchaser'].sum()/len(df_va))
print('Purchase/view rate for control group who uses Accor: ', 0, "For variant group:", 0)
print('Purchase/view rate for control group who uses LATAM ', df_cc['purchaser'].sum()/len(df_cc), "For variant group:", df_vc['purchaser'].sum()/len(df_vc))

print('Overall, the change of the website does not have any effects on any other sections.')

print('In conclusion, the change of website did not affect anything else and made a little contribution '
      'to the purchase/view rate. While such a little contribution means nothing for such a big sample size,  it'
      ' caused a huge drawback on the total booking sales to decease it by 7%. I will not advice you to keep this change for your future use. ')