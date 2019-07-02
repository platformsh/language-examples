package examples

import (
	"database/sql"
	"fmt"
	_ "github.com/go-sql-driver/mysql"
	psh "github.com/platformsh/config-reader-go/v2"
	sqldsn "github.com/platformsh/config-reader-go/v2/sqldsn"
)

func UsageExampleMySQL() string {

	// Create a NewRuntimeConfig object to ease reading the Platform.sh environment variables.
	// You can alternatively use os.Getenv() yourself.
	config, err := psh.NewRuntimeConfig()
	if err != nil {
		panic(err)
	}

	// The 'database' relationship is generally the name of the primary SQL database of an application.
	// That's not required, but much of our default automation code assumes it.
	credentials, err := config.Credentials("database")
	checkErr(err)

	// Using the sqldsn formatted credentials package
	formatted, err := sqldsn.FormattedCredentials(credentials)
	checkErr(err)

	db, err := sql.Open("mysql", formatted)
	checkErr(err)
	defer db.Close()

	// Force MySQL into modern mode.
	db.Exec("SET NAMES=utf8")
	db.Exec("SET sql_mode = 'ANSI,STRICT_TRANS_TABLES,STRICT_ALL_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,ONLY_FULL_GROUP_BY'")

	_, err = db.Exec("DROP TABLE IF EXISTS userinfo")
	checkErr(err)

	_, err = db.Exec(`CREATE TABLE userinfo (
				uid INT(10) NOT NULL AUTO_INCREMENT,
				username VARCHAR(64) NULL DEFAULT NULL,
				departname VARCHAR(128) NULL DEFAULT NULL,
				created DATE NULL DEFAULT NULL,
				PRIMARY KEY (uid)
				) DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;`)
	checkErr(err)

	// insert
	stmt, err := db.Prepare("INSERT userinfo SET username=?,departname=?,created=?")
	checkErr(err)

	res, err := stmt.Exec("platform", "Deploy Friday", "2019-06-17")
	checkErr(err)

	id, err := res.LastInsertId()
	checkErr(err)

	// update
	stmt, err = db.Prepare("update userinfo set username=? where uid=?")
	checkErr(err)

	res, err = stmt.Exec("goPlatformsh", id)
	checkErr(err)

	affect, err := res.RowsAffected()
	checkErr(err)

	// query
	rows, err := db.Query("SELECT * FROM userinfo")
	checkErr(err)

	var uid int
	var username string
	var department string
	var created string
	for rows.Next() {
		err = rows.Scan(&uid, &username, &department, &created)
		checkErr(err)
	}

	// delete
	stmt, err = db.Prepare("delete from userinfo where uid=?")
	checkErr(err)

	res, err = stmt.Exec(id)
	checkErr(err)

	affect, err = res.RowsAffected()
	checkErr(err)

	output := fmt.Sprintf(`Hello, World! - A simple Gin web framework template for Platform.sh

MySQL Tests:

* Connect and add row:
	 - Row ID (1): %d
	 - Username (goPlatformsh): %s
	 - Department (Deploy Friday): %s
	 - Created (2019-06-17): %s
* Delete row:
	 - Status (1): %d

		`, uid, username, department, created, affect)

	return output
}

// checkErr is a simple wrapper for panicking on error.
// It likely should not be used in a real application.
func checkErr(err error) {
	if err != nil {
		panic(err)
	}
}
