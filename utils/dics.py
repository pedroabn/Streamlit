#%% Importando bibliotecas
import streamlit as st
import pandas as pd

recife = ['CURADO', 'DOIS UNIDOS', 'AFLITOS', 'SANCHO', 'VARZEA', 'COELHOS',
 'PEIXINHOS', 'SAO JOSE', 'SANTO ANTONIO', 'RECIFE', 'HIPODROMO', 'ROSARINHO',
 'CAMPINA DO BARRETO', 'CASA FORTE', 'PARNAMIRIM', 'GUABIRABA', 'ILHA JOANA BEZERRA',
 'CABANGA', 'ILHA DO LEITE', 'PAU FERRO', 'MANGUEIRA', 'SANTO AMARO', 'BOA VISTA',
 'ESPINHEIRO', 'DERBY', 'SANTANA', 'PAISSANDU', 'TOTO', 'GRACAS', 'TORRE', 'ARRUDA',
 'ENGENHO DO MEIO', 'CAJUEIRO', 'COHAB - IBURA DE CIMA', 'ZUMBI', 'TAMARINEIRA', 'BONGI',
 'CIDADE UNIVERSITARIA', 'TORREAO', 'JAQUEIRA', 'CACOTE', 'IPSEP', 'PORTO DA MADEIRA', 'JORDAO',
 'PRADO', 'TORROES', 'DOIS IRMAOS', 'MADALENA', 'SOLEDADE', 'IPUTINGA', 'SAN MARTIN', 'JARDIM SAO PAULO',
 'AREIAS', 'MANGABEIRA', 'PASSARINHO', 'TEJIPIO', 'CORDEIRO', 'COQUEIRAL', 'POCO', 'BARRO', 'ESTANCIA',
 'FUNDAO', 'CAXANGA', 'SITIO DOS PINTOS - SAO BRAS', 'BEBERIBE', 'BOMBA DO HEMETERIO', 'CASA AMARELA',
 'LINHA DO TIRO', 'ENCRUZILHADA', 'BRASILIA TEIMOSA', 'ALTO JOSE DO PINHO', 'PINA', 'BREJO DA GUABIRABA', 'ILHA DO RETIRO',
 'MUSTARDINHA', 'MONTEIRO', 'IBURA', 'ALTO JOSE BONIFACIO', 'ALTO DO MANDU', 'MORRO DA CONCEICAO', 'VASCO DA GAMA', 'BOA VIAGEM',
 'ALTO SANTA TEREZINHA', 'CAMPO GRANDE', 'MACAXEIRA', 'NOVA DESCOBERTA', 'BREJO DE BEBERIBE', 'AGUA FRIA', 'IMBIRIBEIRA', 'JIQUIA',
 'AFOGADOS', 'APIPUCOS', 'CORREGO DO JENIPAPO', 'PONTO DE PARADA']



dic_sic_cad = {
    'Fotografia': 'Fotografia',
    'nan': 'Outros',
 'Audiovisual':'Audiovisual' ,
 'Cultura Popular': 'Cultura Popular',
 'Artes Visuais': 'Artes Visuais',
 'Música': 'Música',
 'Literatura':'Literatura' ,
 'Pesquisa E Formação Cultural':'Pesquisa e Formação' ,
 'Design E Moda': 'Moda',
 'Dança': 'Dança',
 'Artesanato': 'Artesanato' ,
 'Patrimônio Cultural E Museologia':'Patrimonio' ,
 'Teatro':'Artes cenicas' ,
 'Artes Culturais Integradas E Arte E Tecnologia':'Artes Integradas' ,
 'Circo': 'Circo',
 'Artes Plásticas E Gráficas': 'Artes Visuais' ,
 'Opera': 'Opera',
 'Gastronomia':'Gastronomia' ,
    
}
