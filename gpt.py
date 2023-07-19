import openai
import os
import json
openai.api_key = os.getenv("OPENAI_API_KEY")


systemPrompt = """
    summarize this content into an overall summary, and a bullet list of special need accommodations, and whether it is TRUE available or FALSE unavailable at this school. make the list comprehensive, not just ones at the school. Always output in JSON format
"""

rawWebsite = """
Special Education

SpEd Website Banner
The Los Gatos Saratoga Union High School District ensures that all students with specialized learning needs are provided with a free and appropriate public education.  Our school sites are staffed with qualified professionals who work together with students and families to ensure that the educational needs and services are provided in the least restrictive environment.  We are proud of the programs we provide and appreciate the efforts of students and families to maximize their educational experience. 
Individualized Education Program (IEP)

Once a student has been assessed, an Individualized Education Program (IEP) meeting is held to determine a student's eligibility for services.  Students may be found to be eligible in one of 13 categories:

Learning Disabilities
Speech and Language Impairment
Deaf-Blind
Visual Impairment
Traumatic Brain Injury
Hearing Impairment
Deafness
Other Health Impairment
Autism
Multiple Disabilities
Orthopedic Impairment
Emotional Disturbance
Intellectual Disability
Services & Programs

Students may receive any combination of services, based on their Individualized Education Program (IEP), including:

Speech and Language Support - Speech and language specialists provide support for articulation, voice, fluency, and language disorders.
Specialized Academic Instruction - Special Education teachers provide educational planning, special instruction, tutorial assistance, or other services to exceptional individuals in special programs or regular classrooms.
Special Day Classes - Students are grouped with others who share similar instructional needs.  Each class has a credentialed special education teacher and an instructional aide.
Adaptive physical education, nursing services, counseling support, behavior support, occupational therapy, and other services are available when a student's IEP determines this need.

Transition to Independent Living

Several of our programs assist with special education needs to transition to the workplace, independent living, and post secondary education or training.

WorkAbility 1 - Workability 1 programs provide comprehensive pre-employment training, employment placement, and follow-up consultations for individuals making the transition to independent living.
Post-Secondary Programs - This Community Immersion Program (CIP) provides services for students with disabilities who have completed high schools through enrollment and participation in an active college atmosphere; and prepares them for independent living, including work, leisure, and academics.
SELPA III Plan
Post Secondary Program
Workability
Contact Us with Questions

Please contact us if we can provide further information about Special Education, 408-354-2520 x239.

Heath Rocha - Assistant Superintendent, Student Services

Tammie Marshall- Administrative Assistant

Bret Schmidt - Program Specialist

Site Administration and Special Education Department Chairs:

Amy Drolette - Assistant Principal (LGHS)

Cabot Weaver- Department Chair (LGHS)

Matt Torrens - Assistant Principal (SHS)

Brian Elliott - Department Chair (SHS)
"""
completion = openai.ChatCompletion.create(
model="gpt-3.5-turbo",
messages=[
    {"role": "system", "content": "Generate some JSON data based on input."},
    {"role": "user", "content": "name=jevon, age,17"}
]
)
response = completion.choices[0].message.content
print(response)
#print(json.loads(response))