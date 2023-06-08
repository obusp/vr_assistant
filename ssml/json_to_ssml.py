import pandas as pd
import xml.etree.cElementTree as ET

def init ():
    global index, sender, subject, summary


    # load json file
    df = pd.read_json (r'Email_JSON.json')
    index    = range(df.index.size)
    sender   = df.sender
    subject  = df.subject
    summary  = df.summary

def data_set(i):
    ordinal = '{}{}'.format(i+1, get_suffix(i+1))
    if i !=len(index)-1:
        if not subject[i] and summary[i]:
            return ('The {} email is from {}, no subject is included and the summary is: {}'.
                    format(ordinal,sender[i], summary[i]))

        elif subject[i] and not summary[i]:
            return ('The {} email is from {} about {}, but there is no summary included.'.
                    format(ordinal,sender[i], subject[i]))

        elif not subject[i] and not summary[i]:
            return ('The {} email is from {}, but no subject neither summary are included.'.
                    format(ordinal,sender[i]))
        else:
            return ('The {} email is from {} about {}, and the summary is: {}'.
                    format(ordinal,sender[i], subject[i], summary[i]))

    else:
        if not subject[i] and summary[i]:
            return ('The {} and last email is from {}, no subject is included and the summary is: {}'.
                    format(ordinal,sender[i], summary[i]))

        elif subject[i] and not summary[i]:
            return ('The {} and last email is from {} about {}, but there is no summary included.'.
                    format(ordinal,sender[i], subject[i]))

        elif not subject[i] and not summary[i]:
            return ('The {} and last email is from {}, but no subject neither summary are included.'.
                    format(ordinal,sender[i]))

        else:
            return ('The {} and last email is from {} about {}, and the summary is: {}'.
                    format(ordinal,sender[i], subject[i], summary[i]))

def get_suffix(num):
    if num in [10, 11, 12, 13]:
        return 'th'
    else:
        rem = num % 10
        if rem == 1:
            return 'st'
        elif rem == 2:
            return 'nd'
        elif rem == 3:
            return 'rd'
        else:
            return 'th'

def root_att():
    attrib = {
        "version": "1.0",
        "xmlns": "http://www.w3.org/2001/10/synthesis",
        "xml:lang": "en-US"
    }
    return attrib


def build_xml ():

    # Voice and sound
    root   = ET.Element("speak", root_att())
    child  = ET.SubElement(root, "voice")
    child.set("name", "en-US-ChristopherNeural")    
    for i in index:
        sentence  = ET.SubElement(child, "s")
        sentence.text = (data_set(i))
        if i !=len(index)-1:
            silence       = ET.SubElement(child, "break")
            silence.set("time","500ms")
        else:
            continue

    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0)
    with open("json_to_ssml.xml", "wb") as f:
        tree.write(f)


if __name__ == '__main__':

    init()
    build_xml()