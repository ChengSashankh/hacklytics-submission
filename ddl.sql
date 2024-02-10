CREATE TABLE "cms" (
  "cpt_code" varchar(16) PRIMARY KEY,
  "procedure" varchar(128),
  "description" varchar(2048)
);

CREATE TABLE "hospitals" (
  "hospital_id" int PRIMARY KEY,
  "hospital_name" varchar2,
  "address" varchar2
);

CREATE TABLE "hospital_general_prices" (
  "cpt_code" varchar2,
  "hospital_id" int,
  "procedure" varchar2,
  "charges" float,
  "discounted_charges" float,
  "min_negotiated" float,
  "max_negotiated" float
);

CREATE TABLE "hospital_insurance_prices" (
  "hospital_id" int,
  "cpt_code" varchar2,
  "provider_id" int,
  "cost" float
);

CREATE TABLE "insurance" (
  "provider_id" int PRIMARY KEY,
  "provider_name" varchar2
);

ALTER TABLE "hospital_general_prices" ADD FOREIGN KEY ("cpt_code") REFERENCES "cms" ("cpt_code");

ALTER TABLE "hospital_general_prices" ADD FOREIGN KEY ("hospital_id") REFERENCES "hospitals" ("hospital_id");

ALTER TABLE "hospital_insurance_prices" ADD FOREIGN KEY ("hospital_id") REFERENCES "hospitals" ("hospital_id");

ALTER TABLE "hospital_insurance_prices" ADD FOREIGN KEY ("cpt_code") REFERENCES "cms" ("cpt_code");

ALTER TABLE "hospital_insurance_prices" ADD FOREIGN KEY ("provider_id") REFERENCES "insurance" ("provider_id");
