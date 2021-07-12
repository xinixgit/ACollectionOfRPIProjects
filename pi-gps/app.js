const SerialPort = require("serialport");
const SerialPortParser = require("@serialport/parser-readline");
const GPS = require("gps");
const Request = require("request-promise");
const mysql = require('mysql');

const port = new SerialPort("/dev/serial0", { baudRate: 9600 });
const gps = new GPS();

const parser = port.pipe(new SerialPortParser());

const argv = require('minimist')(process.argv.slice(2));
const username = argv['u']
const password = argv['p']

const conn = mysql.createConnection({
  host: "localhost",
  user: username,
  password: password,
  database: "exports"
});

conn.connect(function(err) {
  if (err) throw err;
  console.log("Connected!");
});

const stmt = "insert into gps_loc(lat, lng, ts_epoch, t_created, alt, geoidal, valid) VALUES (?, ?, ?, ?, ?, ?, ?)";

function insert_coordinates(data, conn) {
	const time = data.time
	const epoch = Math.floor(time.getTime() / 1000)
	const params = [
		data.lat,
		data.lon,
		epoch,
		time.toISOString(),
		(data.alt || '').toString(),
		(data.geoidal || '').toString(),
		(data.valid || '').toString()
	]

	conn.query(stmt, params, (err, res, fields) => {
		if (err) {
			return console.error(err.message);
		}
	})
}

function sleep(timeInMs) {
	return new Promise(resolve => setTimeout(resolve, timeInMs));
}

gps.on("data", async data => {
  if(data.type == "GGA") {
    if(data.quality != null) {
      insert_coordinates(data, conn);
    }
  }
});

// when data comes in from the serial port, use the gps module to parse it
parser.on("data", data => {
  try {
    gps.update(data);
  } catch (e) {
    throw e;
  }
});