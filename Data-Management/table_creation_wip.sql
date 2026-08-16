-- create brand table
CREATE TABLE brand (
	brand_id SERIAL NOT NULL PRIMARY KEY,
	brand_name VARCHAR(255) NOT NULL
);

-- import brands
\copy brand(brand_name) FROM '/Users/andrewstringer/Downloads/Scenario 1/brand table.csv' WITH (FORMAT CSV, HEADER, DELIMITER ',');

-- create display table
CREATE TABLE display (
	display_id SERIAL NOT NULL PRIMARY KEY,
	display_type VARCHAR(255) NOT NULL
);

-- import display types
\copy display(display_type) FROM '/Users/andrewstringer/Downloads/Scenario 1/display table.csv' WITH (FORMAT CSV, HEADER, DELIMITER ',');

-- create strap table
CREATE TABLE strap (
	strap_id SERIAL NOT NULL PRIMARY KEY,
	strap_material VARCHAR(255) NOT NULL
);

-- import strap materials
\copy strap(strap_material) FROM '/Users/andrewstringer/Downloads/Scenario 1/strap table.csv' WITH (FORMAT CSV, HEADER, DELIMITER ',');

-- create tracker table
CREATE TABLE tracker (
	tracker_id BIGSERIAL NOT NULL PRIMARY KEY,
	brand_id INT NOT NULL REFERENCES brand(brand_id),
	device_type VARCHAR(255),
	model_name VARCHAR(255) NOT NULL,
	color VARCHAR(255),
	selling_price NUMERIC,
	original_price NUMERIC,
	display_id INT NOT NULL REFERENCES display(display_id),
	rating NUMERIC,
	strap_id INT NOT NULL REFERENCES strap(strap_id),
	average_battery_life INT,
	reviews INT
	brand_name VARCHAR(255) NOT NULL,
	display_type VARCHAR(255) NOT NULL,
	strap_material VARCHAR(255) NOT NULL
);

-- import trackers
\copy tracker(brand_id, device_type, model_name, color, selling_price, original_price, display_id, rating, strap_id, average_battery_life, reviews, brand_name, display_type, strap_material)  FROM '/Users/andrewstringer/Downloads/Scenario 1/tracker table.csv'  WITH (FORMAT CSV, HEADER, DELIMITER ',');

-- update tracker table for dynamic data from brand table
UPDATE tracker
SET brand_id = (SELECT brand_id FROM brand WHERE brand_name = tracker.brand_name)
WHERE brand_id = 2;

-- update tracker table for dynamic data from display table
UPDATE tracker
SET display_id = (SELECT display_id FROM display WHERE display_type = tracker.display_type)
WHERE display_id = 2;

-- update tracker table for dynamic data from strap table
UPDATE tracker
SET strap_id = (SELECT strap_id FROM strap WHERE strap_material = tracker.strap_material)
WHERE strap_id = 25;

-- remove the extra columns used for importing
ALTER TABLE tracker
DROP COLUMN brand_name,
DROP COLUMN display_type,
DROP COLUMN strap_material;

-- create patient table
CREATE TABLE patient (
	patient_id BIGSERIAL NOT NULL PRIMARY KEY,
	first_name VARCHAR(255) NOT NULL,
	last_name VARCHAR(255) NOT NULL,
	date_of_birth DATE NOT NULL,
	gender VARCHAR(255) NOT NULL,
	medical_condition VARCHAR(255) NOT NULL,
	medication VARCHAR(255) NOT NULL,
	allergy VARCHAR(255) NOT NULL,
	last_appointment_date DATE NOT NULL,
	tracker_id BIGINT REFERENCES tracker(tracker_id),
	model_name VARCHAR(255) NOT NULL
);

-- import patient info
\copy patient(first_name, last_name, date_of_birth, gender, medical_condition, medication, allergy, last_appointment_date, tracker_id, model_name) FROM '/Users/andrewstringer/Downloads/Scenario 1/patient table.csv' WITH (FORMAT CSV, HEADER, DELIMITER ',');

-- update patient table for dynamic data from tracker table
UPDATE patient
SET tracker_id = (SELECT tracker_id FROM tracker WHERE model_name = patient.model_name LIMIT 1)
WHERE tracker_id = 2083;

-- remove the extra column from importing
ALTER TABLE patient
DROP COLUMN model_name;