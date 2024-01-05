import sys, getopt, os, subprocess, random, string, sqlite3


def get_random_end():
    try:
        int_random = random.randint(32, 52)
        ret = ''.join(random.sample(string.ascii_letters + string.digits, int_random))
    except Exception, e:
        print(e)
    return ret


def change_sqlite3_db_content(db_path=None):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        name = ''.join(random.sample(string.ascii_letters, 4))
        user = ''.join(random.sample(string.ascii_letters, 4))
        michael = ''.join(random.sample(string.ascii_letters, 7))
        cursor.execute('CREATE TABLE %s (id VARCHAR(20) PRIMARY KEY, %s VARCHAR(20))' % (user, name))
        cursor.execute('insert into %s (id, %s) values (\'1\', \'%s\')' % (user, name, michael))
        cursor.rowcount
        cursor.close()
        conn.commit()
        conn.close()
    except Exception, e:
        print(e)


def run_cmd(cmd=None):
    try:
        print(cmd)
        ret = subprocess.check_output(cmd, shell=True)
        return ret
    except Exception, e:
        print(e)
        return e.output


def change_file_hash(project_path=None):
    print('UUProcess: change resource file hash')

    os.chdir(project_path)

    file_type_array = ['*.png', '*.jpg', '*.JPG', '*.gif', '*.mp4', '*.mp3']

    # for file_name in file_type_array:
    #     files_string = run_cmd('find . -iname "%s"' % (file_name))
    #     files = files_string.split('\n')
    #     for file in files:
    #         if '' == file: continue
    #         salt = get_random_end()
    #         run_cmd('echo "%s" >> "%s"' % (salt, file))

    db_type_array = ['*.sqlite', '*.db']
    for db_name in db_type_array:
        files_string = run_cmd('find . -iname "%s"' % (db_name))
        files = files_string.split('\n')
        for file in files:
            if '' == file: continue
            change_sqlite3_db_content(file)


def run():
    opts, args = getopt.getopt(sys.argv[1:], "p:")

    for op, value in opts:
        # u3d project path
        if op == '-p':
            project_path = value
    if not project_path:
        print("UUProcess: no args for -p")
    change_file_hash(project_path=project_path)


if __name__ == "__main__":
    # run()
    project_path = '/Users/ganyuanrong/unitypro/New Unity Project'
    change_file_hash(project_path=project_path)