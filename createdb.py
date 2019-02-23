import pymysql

conn = pymysql.connect("localhost", "monitor", "*hope8848", "monitordb")
print("Opened database successfully")

cur = conn.cursor()
cur.execute("""CREATE TABLE cpu (
  id serial primary key,
  logicalCount varchar(16),
  physicalCount varchar(16),
  userFreetime varchar(16),
  sysFreetime varchar(16),
  allPercent varchar(16))""")
cur.execute("""ALTER TABLE `cpu` ADD `create` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;""")
print("Table cpu created successfully")

cur.execute("""CREATE TABLE mem (
  id serial primary key,
  memTotal varchar(16),
  memAvailable varchar(16),
  memPercent varchar(16),
  memUsed varchar(16),
  memFree varchar(16))""")
cur.execute("""ALTER TABLE `mem` ADD `create` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;""")
print("Table mem created successfully")

cur.execute("""CREATE TABLE disk (
  id serial primary key,
  diskTotal varchar(16),
  diskUsed varchar(16),
  diskFree varchar(16),
  diskPercent varchar(16))""")
cur.execute("""ALTER TABLE `disk` ADD `create` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;""")
print("Table disk created successfully")

cur.execute("""CREATE TABLE net (
  id serial primary key,
  device varchar(15),
  addrs varchar(15))""")
cur.execute("""ALTER TABLE `net` ADD `create` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;""")
print("Table net created successfully")

cur.execute("""CREATE TABLE boot_time (
  id serial primary key,
  boot_time varchar(25))""")
cur.execute("""ALTER TABLE `boot_time` ADD `create` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;""")
print("Table boot_time created successfully")

conn.commit()
conn.close()