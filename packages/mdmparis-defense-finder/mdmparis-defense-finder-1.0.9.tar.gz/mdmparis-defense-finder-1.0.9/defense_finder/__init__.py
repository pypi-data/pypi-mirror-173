import subprocess

def run(f, dbtype, workers, tmp_dir, models_dir, nocut_ga):
    arg_nocut = "--no-cut-ga" if nocut_ga else ""
    arg_dir = f"--models-dir {models_dir}" if models_dir is not None else ""

    script = f"""
macsyfinder --db-type {dbtype} --sequence-db "{f.name}" --models defense-finder-models/DefenseFinder_1 all --out-dir {tmp_dir}/DF_1 --coverage-profile 0.1  --w {workers} --exchangeable-weight 1 {arg_dir} {arg_nocut}
macsyfinder --db-type {dbtype} --sequence-db "{f.name}" --models defense-finder-models/DefenseFinder_2 all --out-dir {tmp_dir}/DF_2 --coverage-profile 0.1  --w {workers} --exchangeable-weight 1 {arg_dir} {arg_nocut}
macsyfinder --db-type {dbtype} --sequence-db "{f.name}" --models defense-finder-models/DefenseFinder_3 all --out-dir {tmp_dir}/DF_3 --coverage-profile 0.1  --w {workers} --exchangeable-weight 1 {arg_dir} {arg_nocut}
macsyfinder --db-type {dbtype} --sequence-db "{f.name}" --models defense-finder-models/DefenseFinder_4 all --out-dir {tmp_dir}/DF_4 --coverage-profile 0.1  --w {workers} --exchangeable-weight 1 {arg_dir} {arg_nocut}
macsyfinder --db-type {dbtype} --sequence-db "{f.name}" --models defense-finder-models/DefenseFinder_5 all --out-dir {tmp_dir}/DF_5 --coverage-profile 0.1  --w {workers} --exchangeable-weight 1 {arg_dir} {arg_nocut}
macsyfinder --db-type {dbtype} --sequence-db "{f.name}" --models defense-finder-models/RM all --out-dir {tmp_dir}/RM --coverage-profile 0.1  --w {workers} --exchangeable-weight 1 {arg_dir} {arg_nocut}
macsyfinder --db-type {dbtype} --sequence-db "{f.name}" --models defense-finder-models/Cas all --out-dir {tmp_dir}/Cas --accessory-weight 1 --exchangeable-weight 1 --coverage-profile 0.4 -w {workers} {arg_dir} {arg_nocut}
"""
    subprocess.run(script, shell=True)
