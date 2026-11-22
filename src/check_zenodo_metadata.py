from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
c=json.loads((R/'results/certificate_d72.json').read_text('utf8'))
m=json.loads((R/'publication/zenodo_metadata_blueprint.json').read_text('utf8'))
assert c['status']=='PASS' and c['dimension']==m['scientific_dimension']==72
assert c['vertices']==m['norm_one_vertices']==77
assert c['pairs']==m['exact_labelled_squared_pairs']==2926
assert c['affine_rank']==c['centered_gram_rank']==72
assert c['eigenvalue_77_over_2_multiplicity']==m['model_eigenvalue_77_over_2_multiplicity']==66
assert c['eigenvalue_38_multiplicity']==m['model_eigenvalue_38_multiplicity']==4
assert c['parent_tag_commit']=='8a8aa86038ba6d6555590173edd89982c3e38889'
assert c['parent_doi']==m['scientific_parent_doi']=='10.5281/zenodo.24433507'
assert m['related_identifiers']==[{'identifier':c['parent_doi'],'relation':'isDerivedFrom','resource_type':'publication-preprint','scheme':'doi'}]
assert len(m['keywords'])==9 and len(set(m['keywords']))==9
assert 'affine Euclidean dimension seventy-two' in m['keywords'] and 'sixty-sixfold ideal eigenvalue' in m['keywords']
assert not set(m['keywords']).intersection({'affine Euclidean dimension seventy-one','sixty-fivefold ideal eigenvalue','affine Euclidean dimension seventy-three','sixty-sevenfold ideal eigenvalue'})
assert len(m['references'])==2 and c['parent_doi'] in m['references'][0] and '10.5281/zenodo.24407952' in m['references'][1]
assert all(x in (R/'publication/POLYBRUTUS_72D_NOTE.md').read_text('utf8') for x in ('## References',c['parent_doi'],'10.5281/zenodo.24407952'))
print('D72 METADATA 9 KEYWORDS / 2 REFERENCES / DIRECT D71 DOI PASS')
