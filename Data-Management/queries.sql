SELECT *
FROM patient
WHERE medical_condition = 'Watch';

SELECT *
FROM patient
WHERE medical_condition = 'Watch' AND allergy = 'None';

SELECT *
FROM patient
WHERE medical_condition = 'Watch' AND allergy = 'None' AND medication = 'Yes';