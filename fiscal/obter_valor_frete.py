import requests
import xml.etree.ElementTree as ET


def get_vtprest(url):
    response = requests.get(url)
    if response.status_code == 200:
        xml_content = response.content
        
        # Parse do XML
        root = ET.fromstring(xml_content)
        
        # Remover namespaces para facilitar a busca
        for elem in root.iter():
            if '}' in elem.tag:
                elem.tag = elem.tag.split('}', 1)[1]
        
        # Buscar a tag <vTPrest>
        valor_vTPrest = root.find(".//vTPrest")
        
        if valor_vTPrest is not None:
            return valor_vTPrest.text
        else:
            return "Tag <vTPrest> não encontrada."
    else:
        return f"Erro ao baixar o XML: {response.status_code}"