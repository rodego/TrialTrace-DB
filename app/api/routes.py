from flask import Blueprint, jsonify
from flask_restful import Resource, Api



api = Blueprint('api', __name__, url_prefix='/api')
rest = Api(api)

class Example(Resource):
  def get(self):
    return {'data':[
      {
        "Rank":1,
        "NCTId":
          "NCT03863457"
        ,
        "BriefTitle":
          "[18F] F-GLN by PET/CT in Breast Cancer"
        ,
        "Condition":
          "Breast Cancer"
        ,
        "BriefSummary":
          "Patients with known or suspected primary or metastatic breast cancer with one lesion that is 1.5 cm in diameter or greater may be eligible for this study. Patients may participate in this study if they are at least 18 years of age. Up to 40 evaluable subjects will participate in a single imaging cohort. Patients will be stratified for analysis by breast cancer subtype with prioritization to recruit at least 10 estrogen-receptor-expressing (ER+) and 10 triple-negative breast cancers (TNBC).\n\nThis is an observational study; [18F]F-GLN PET/CT will not be used to direct treatment decisions. While patients and referring physicians will not be blinded to the [18F]F-GLN PET/CT results, treatment decisions are made by the treating physicians based upon clinical criteria.\n\n[18F]F-GLN PET/CT imaging sessions will include an injection of [18F]F-GLN. Metabolism data will be collected. Pilot data will be collected to evaluate image quality and collect preliminary information on the uptake of [18F]F-GLN in breast cancer. Uptake measures will be compared to tumor markers of glutamine metabolism, when tissue is available. The safety of [18F]F-GLN will also be evaluated in all subjects."
        ,
        "EligibilityCriteria":
          "Inclusion Criteria:\n\nParticipants will be ≥ 18 years of age\nKnown or suspected primary or metastatic breast cancer.\nAt least one lesion ≥ 1.5 cm that is seen on standard imaging (e.g. CT, MRI, mammogram, ultrasound, FDG-PET/CT). Only one type of imaging is required to show a lesion.\nParticipants must be informed of the investigational nature of this study and be willing to provide written informed consent and participate in this study in accordance with institutional and federal guidelines prior to study-specific procedures.\n\nExclusion Criteria:\n\nFemales who are pregnant or breast feeding at the time of screening; a urine pregnancy test will be performed in women of child-bearing potential at screening.\nInability to tolerate imaging procedures in the opinion of an investigator or treating physician.\nAny current medical condition, illness, or disorder, as assessed by medical record review and/or self-reported, that is considered by a physician investigator to be a condition that could compromise participant safety or successful participation in the study."
        
      }
    ]
    }

rest.add_resource(Example, '/')
