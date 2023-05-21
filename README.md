# OZON PARSER

## Installation

```bash=
cd your/code/folder
git clone https://github.com/boldueen/ozon_parser.git
cd ozon_parser
python3.10 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

`add your config.json file (for enable gsheets)`
and set config.json name to config.py
`SERVICE_FILE = r'./YOUT_CONFIG_FILENAME.json'`

`remove unused files`

```bash
rm ./data/category_fees/delete_after_install.txt
rm ./data/fbo_fbs/delete_after_install.txt
```

### run fbo_fbs parser

```bash
. venv/bin/activate
python parser_fbo_fbs.py
```

parsed data will be in ./data/fbo_fbs

### run fbo_fbs parser

```bash
. venv/bin/activate
python parser_category_fee.py
```

parsed data will be in ./data/category_fees
