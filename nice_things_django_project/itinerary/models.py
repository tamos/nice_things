import datetime
from django.db import models
from django.utils import timezone


'''class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now()


datetime.timedelta(days=1)'''


'''class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text'''


class Flag(models.Model):
    flag_type = models.CharField(max_length=200)
    flag_count = models.IntegerField(default=0)
    longitude_trunc = models.FloatField()
    latitude_trunc = models.FloatField()


class Food(models.Model):
    inspection_id = models.PositiveIntegerField(primary_key=True)
    dba_name = models.CharField(max_length=200)
    aka_name = models.CharField(max_length=200)
    license_num = models.PositiveIntegerField()
    facility_type = models.CharField(max_length=200)
    '''risk = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=2)
    zip = models.IntegerField()
    date = models.DateTimeField()
    inspection_type = models.CharField(max_length=200)
    result = models.CharField(max_length=200)
    violations = models.TextField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    #longitude_trunc = models.ForeignKey(Flag, on_delete=models.CASCADE)
    #latitude_trunc = models.ForeignKey(Flag, on_delete=models.CASCADE)
    flag_type = models.CharField(max_length=200)'''


class Wages(models.Model):
    case_id = models.PositiveIntegerField(primary_key=True)
    trade_nm = models.CharField(max_length=200)
    legal_name = models.CharField(max_length=200)
    street_addr_1_txt = models.CharField(max_length=200)
    cty_nm = models.CharField(max_length=200)
    st_cd = models.CharField(max_length=2)
    zip_cd = models.CharField(max_length=200)
    case_violtn_cnt = models.PositiveIntegerField()
    longitude_trunc = models.FloatField()
    latitude_trunc = models.FloatField()

    '''naic_cd
    naics_code_description

    cmp_assd_cnt
    ee_violtd_cnt
    bw_atp_amt
    ee_atp_cnt
    findings_start_date
    findings_end_date
    flsa_violtn_cnt
    flsa_repeat_violator
    flsa_bw_atp_amt
    flsa_ee_atp_cnt
    flsa_mw_bw_atp_amt
    flsa_ot_bw_atp_amt
    flsa_15a3_bw_atp_amt
    flsa_cmp_assd_amt
    sca_violtn_cnt
    sca_bw_atp_amt
    sca_ee_atp_cnt
    mspa_violtn_cnt
    mspa_bw_atp_amt
    mspa_ee_atp_cnt
    mspa_cmp_assd_amt
    h1b_violtn_cnt
    h1b_bw_atp_amt
    h1b_ee_atp_cnt
    h1b_cmp_assd_amt
    fmla_violtn_cnt
    fmla_bw_atp_amt
    fmla_ee_atp_cnt
    fmla_cmp_assd_amt
    flsa_cl_violtn_cnt
    flsa_cl_minor_cnt
    flsa_cl_cmp_assd_amt
    dbra_cl_violtn_cnt
    dbra_bw_atp_amt
    dbra_ee_atp_cnt
    h2a_violtn_cnt
    h2a_bw_atp_amt
    h2a_ee_atp_cnt
    h2a_cmp_assd_amt
    flsa_smw14_violtn_cnt
    flsa_smw14_bw_amt
    flsa_smw14_ee_atp_cnt
    cwhssa_violtn_cnt
    cwhssa_bw_amt
    cwhssa_ee_cnt
    osha_violtn_cnt
    osha_bw_atp_amt
    osha_ee_atp_cnt
    osha_cmp_assd_amt
    eppa_violtn_cnt
    eppa_bw_atp_amt
    eppa_ee_cnt
    eppa_cmp_assd_amt
    h1a_violtn_cnt
    h1a_bw_atp_amt
    h1a_ee_atp_cnt
    h1a_cmp_assd_amt
    crew_violtn_cnt
    crew_bw_atp_amt
    crew_ee_atp_cnt
    crew_cmp_assd_amt
    ccpa_violtn_cnt
    ccpa_bw_atp_amt
    ccpa_ee_atp_cnt
    flsa_smwpw_violtn_cnt
    flsa_smwpw_bw_atp_amt
    flsa_smwpw_ee_atp_cnt
    flsa_hmwkr_violtn_cnt
    flsa_hmwkr_bw_atp_amt
    flsa_hmwkr_ee_atp_cnt
    flsa_hmwkr_cmp_assd_amt
    ca_violtn_cnt
    ca_bw_atp_amt
    ca_ee_atp_cnt
    pca_violtn_cnt
    pca_bw_atp_amt
    pca_ee_atp_cnt
    flsa_smwap_violtn_cnt
    flsa_smwap_bw_atp_amt
    flsa_smwap_ee_atp_cnt
    flsa_smwft_violtn_cnt
    flsa_smwft_bw_atp_amt
    flsa_smwft_ee_atp_cnt
    flsa_smwl_violtn_cnt
    flsa_smwl_bw_atp_amt
    flsa_smwl_ee_atp_cnt
    flsa_smwmg_violtn_cnt
    flsa_smwmg_bw_atp_amt
    flsa_smwmg_ee_atp_cnt
    flsa_smwsl_violtn_cnt
    flsa_smwsl_bw_atp_amt
    flsa_smwsl_ee_atp_cnt
    eev_violtn_cnt
    h2b_violtn_cnt
    h2b_bw_atp_amt
    h2b_ee_atp_cnt
    sraw_violtn_cnt
    sraw_bw_atp_amt
    sraw_ee_atp_cnt
    ld_dt'''






