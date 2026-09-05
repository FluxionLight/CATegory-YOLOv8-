// 导入 axios配置
import request from "../utils/request"



export const predictBreed = (data: any) => request({
    url: '/predictBreed',
    method: 'post',
    data
});


export const getBreedInfo = async (breedName: string) => {
    try {
        const resource = 'http://dbpedia.org/resource/' + breedName.replace(/\s+/g, '_');

        const sparqlQuery = `
            PREFIX dbo: <http://dbpedia.org/ontology/>
            SELECT ?abstract  
            WHERE { 
                <${resource}> dbo:abstract ?abstract .
                FILTER(LANG(?abstract) = 'zh')  
            }
        `;

        // 修改请求头和参数
        const response = await fetch(
            'https://dbpedia.org/sparql?' + new URLSearchParams({
                query: sparqlQuery,
                format: 'json'
            }), {
                headers: {
                    'Accept': 'application/sparql-results+json'
                }
            });

        const data = await response.json();

        if (data.results.bindings.length > 0) {
            return data.results.bindings[0].abstract.value;
        }

        return null;
    } catch (error) {
        console.error('Error fetching breed info:', error);
        return null;
    }
};