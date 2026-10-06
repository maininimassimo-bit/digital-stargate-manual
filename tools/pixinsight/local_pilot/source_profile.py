"""Owner-declared source profiles and bounded local inventory, never native processing."""
import copy
import re
import struct
from pathlib import Path
import xml.etree.ElementTree as ET

from .broker import require
from .worker import digest

MODES = {'LRGB': ('R', 'G', 'B', 'L'), 'SHO': ('SII', 'Ha', 'OIII'),
         'HOO': ('Ha', 'OIII'), 'OSC': ('RGB',), 'OSC_CFA': ('CFA',)}
ALIASES = {'R': {'r','red','rosso'}, 'G': {'g','green','verde'}, 'B': {'b','blue','blu'},
           'L': {'l','lum','luminance','luminanza'}, 'Ha': {'ha','halpha','hα'},
           'SII': {'sii','s2'}, 'OIII': {'oiii','o3'}, 'RGB': {'rgb','osc','color','colour'},
           'CFA': {'cfa','bayer','osc'}}
PATTERNS = {'RGGB', 'BGGR', 'GBRG', 'GRBG'}


def selected_panels(selection, plan):
    """Bind assistant file/index proposals to the immutable Owner folder/session scope.

    Returns a derived inspection selection; never mutates the original intake and
    grants no native execution authority. Local headers/hashes are checked separately.
    """
    profile = source_profile(selection)
    require(profile['layout'] == 'PANELS', 'MOSAIC_SOURCE_PLAN_REQUIRED')
    require(isinstance(plan,dict) and set(plan) == {'panels','rationale','limitations'}, 'SOURCE_PLAN_FIELDS')
    require(all(isinstance(plan[k],str) and 1 <= len(plan[k].strip()) <= 4000 for k in ('rationale','limitations')),
            'SOURCE_PLAN_EXPLANATION')
    panels = plan['panels']
    require(isinstance(panels,list) and 2 <= len(panels) <= 16, 'MOSAIC_PANEL_COUNT')
    derived = copy.deepcopy(selection)
    derived['sourceProfile'] = copy.deepcopy(profile)
    descriptors, mappings, identities = [], [], set()
    for panel in panels:
        require(isinstance(panel,dict) and set(panel) == {'panelId','directory','sessionIds','masters'}, 'SOURCE_PLAN_PANEL_FIELDS')
        from .intake import local_directory
        local_directory(panel['directory'])
        descriptors.append({k:copy.deepcopy(panel[k]) for k in ('panelId','directory','sessionIds')})
        mapping = panel['masters']
        require(isinstance(mapping,dict) and set(mapping) == set(MODES[profile['mode']]), 'SOURCE_ROLE_MAPPING')
        for entry in mapping.values():
            require(isinstance(entry,dict) and set(entry) == {'filename','imageIndex'}, 'SOURCE_ROLE_MAPPING')
            name,index = entry['filename'],entry['imageIndex']
            require(isinstance(name,str) and 1 <= len(name) <= 255 and name.lower().endswith('.xisf') and
                    not any(c in name for c in '/\\:*?"<>|') and not any(ord(c)<32 for c in name) and
                    not name.endswith((' ','.')), 'ROLE_FILENAME')
            require(type(index) is int and 0 <= index < 16, 'MASTER_IMAGE_INDEX')
            identity = (panel['directory'].replace('/','\\').casefold(),name.casefold(),index)
            require(identity not in identities, 'MOSAIC_SOURCE_REUSED_AS_ANOTHER_PANEL')
            identities.add(identity)
        mappings.append(copy.deepcopy(mapping))
    derived['sourceProfile']['panels'] = descriptors
    source_profile(derived)
    return derived,mappings


def source_profile(selection):
    # Old saved requests remain readable and retain their original schema/hash.
    profile = selection.get('sourceProfile', {'mode':'LRGB','layout':'SINGLE','bayerPattern':None,'panels':[]})
    fields = {'mode','layout','bayerPattern','panels'}
    require(isinstance(profile, dict) and set(profile) in (fields, fields | {'additionalDirectories'}), 'SOURCE_PROFILE_FIELDS')
    require(profile['mode'] in MODES and profile['layout'] in {'SINGLE','PANELS'}, 'SOURCE_PROFILE_MODE')
    require(profile['bayerPattern'] in PATTERNS if profile['mode'] == 'OSC_CFA' else profile['bayerPattern'] is None,
            'EXPLICIT_BAYER_PATTERN_REQUIRED')
    panels = profile['panels']
    require(isinstance(panels, list), 'MOSAIC_PANELS')
    from .intake import local_directory
    additional = profile.get('additionalDirectories', [])
    require(isinstance(additional,list) and len(additional) <= 15, 'SOURCE_DIRECTORY_COUNT')
    directories = [selection['masterDirectory']] + additional
    for directory in directories:
        local_directory(directory)
    require(len({d.replace('/','\\').rstrip('\\').casefold() for d in directories}) == len(directories),
            'SOURCE_DUPLICATE_DIRECTORY')
    if profile['layout'] == 'SINGLE':
        require(not panels and not additional, 'SINGLE_PANEL_LIST')
        return profile
    if not panels:
        # Discovery may begin with a shared folder containing several panels/filter sets.
        # No assembly or execution authority is granted until explicit selection/plan.
        return profile
    require(2 <= len(panels) <= 16, 'MOSAIC_PANEL_COUNT')
    covered, identifiers = set(), set()
    for panel in panels:
        require(isinstance(panel, dict) and set(panel) == {'panelId','directory','sessionIds'}, 'MOSAIC_PANEL_FIELDS')
        require(isinstance(panel['panelId'],str) and re.fullmatch(r'[A-Za-z0-9_-]{1,40}', panel['panelId']) and
                panel['panelId'] not in identifiers, 'MOSAIC_PANEL_ID')
        identifiers.add(panel['panelId'])
        directory = panel['directory']
        local_directory(directory)
        require(directory in directories, 'MOSAIC_PANEL_OUTSIDE_DECLARED_DIRECTORIES')
        sessions = panel['sessionIds']
        require(isinstance(sessions, list) and sessions and len(sessions) == len(set(sessions)) and
                set(sessions) <= set(selection['sessionIds']), 'MOSAIC_PANEL_SESSIONS')
        covered.update(sessions)
    require(covered == set(selection['sessionIds']), 'MOSAIC_SESSION_COVERAGE')
    require(selection['masterDirectory'] == panels[0]['directory'], 'MOSAIC_FIRST_DIRECTORY_BINDING')
    return profile


def image_metadata(path, mode, index=None):
    with path.open('rb') as stream:
        require(stream.read(8) == b'XISF0100', 'MASTER_XISF')
        header = stream.read(8)
        require(len(header) == 8, 'MASTER_HEADER')
        length, reserved = struct.unpack('<II', header)
        require(0 < length <= 4*1024*1024 and reserved == 0, 'MASTER_HEADER_LIMIT')
        raw = stream.read(length)
    require(len(raw) == length and b'<!DOCTYPE' not in raw and b'<!ENTITY' not in raw, 'MASTER_HEADER')
    images = [e for e in ET.fromstring(raw) if e.tag.split('}')[-1] == 'Image']
    require(1 <= len(images) <= 16, 'MASTER_IMAGES')
    if index is None:
        require(len(images) == 1, 'MULTI_IMAGE_REQUIRES_EXPLICIT_INDEX')
        index = 0
    require(type(index) is int and 0 <= index < len(images), 'MASTER_IMAGE_INDEX')
    image = images[index]
    require(image.get('id') not in {'rejection_low','rejection_high','slope_map','weight_map'}, 'AUXILIARY_IMAGE_NOT_MASTER')
    geometry = image.get('geometry','').split(':')
    require(len(geometry) == 3 and all(re.fullmatch(r'[0-9]+', x) for x in geometry), 'MASTER_GEOMETRY')
    width, height, channels = map(int, geometry)
    expected = 3 if mode == 'OSC' else 1
    require(1 <= width <= 12000 and 1 <= height <= 12000 and channels == expected and
            image.get('sampleFormat') == 'Float32' and image.get('colorSpace') == ('RGB' if expected == 3 else 'Gray'),
            'MASTER_PROFILE_CHANNELS_FLOAT32')
    return {'imageIndex':index,'width':width,'height':height,'channels':channels,
            'sampleFormat':'Float32','colorSpace':'RGB' if channels == 3 else 'Gray'}


def inspect_sources(intake, mappings=None):
    """Inspect each declared directory only; no inferred CFA, panel order or image index."""
    from .intake import local_directory
    selection = intake['selection']
    profile = source_profile(selection)
    require(profile['layout'] != 'PANELS' or bool(profile['panels']), 'MOSAIC_SELECTION_PLAN_REQUIRED')
    panels = profile['panels'] if profile['layout'] == 'PANELS' else [
        {'directory':selection['masterDirectory'],'sessionIds':selection['sessionIds']}]
    require(mappings is None or (isinstance(mappings, list) and len(mappings) == len(panels)), 'PANEL_MAPPING_COUNT')
    output = []
    selected_sources = set()
    for ordinal, panel in enumerate(panels):
        directory = Path(local_directory(panel['directory'])).resolve(strict=True)
        local_directory(str(directory))
        require(directory.is_dir(), 'MASTER_DIRECTORY_MISSING')
        mapping = mappings[ordinal] if mappings else None
        roles = MODES[profile['mode']]
        require(mapping is None or (isinstance(mapping,dict) and set(mapping) == set(roles)), 'SOURCE_ROLE_MAPPING')
        rows = []
        for role in roles:
            if mapping is not None:
                entry = mapping[role]
                require(isinstance(entry,dict) and set(entry) == {'filename','imageIndex'}, 'SOURCE_ROLE_MAPPING')
                name = entry['filename']
                require(isinstance(name,str) and name not in {'.','..'} and not any(c in name for c in '/\\:'), 'ROLE_FILENAME')
                path, index = directory / name, entry['imageIndex']
            else:
                candidates = [p for p in directory.iterdir() if p.is_file() and p.suffix.lower() == '.xisf' and
                              set(re.findall(r'[a-z0-9α]+', p.stem.lower())) & ALIASES[role]]
                # A single OSC file needs no filename role token, but its RGB/CFA metadata is still checked.
                if not candidates and len(roles) == 1:
                    candidates = [p for p in directory.iterdir() if p.is_file() and p.suffix.lower() == '.xisf']
                require(len(candidates) == 1, 'AMBIGUOUS_ROLES_EXPLICIT_MAPPING_REQUIRED')
                path, index = candidates[0], None
            require(not path.is_symlink() and not path.is_junction() and path.suffix.lower() == '.xisf' and
                    path.resolve(strict=True).parent == directory, 'MASTER_OUTSIDE_SELECTED_DIRECTORY')
            metadata = image_metadata(path, profile['mode'], index)
            identity = (path.resolve(strict=True),metadata['imageIndex'])
            require(identity not in selected_sources, 'MOSAIC_SOURCE_REUSED_AS_ANOTHER_PANEL')
            selected_sources.add(identity)
            rows.append({'role':role,'path':path.as_posix(),'sha256':digest(path),**metadata})
        require(len({r['path'] for r in rows}) == len(roles) and
                len({(r['width'],r['height']) for r in rows}) == 1, 'MASTER_ROLES_GEOMETRY')
        output.append({'ordinal':ordinal+1,'directory':directory.as_posix(),'sessionIds':panel['sessionIds'],'masters':rows})
    return {'profile':profile,'panels':output,'authority':'PLANNING_ONLY',
            'linearity':'NATIVE_REVIEW_REQUIRED','registration':'NATIVE_REVIEW_REQUIRED',
            'mosaicOverlap':'NATIVE_REVIEW_REQUIRED' if profile['layout'] == 'PANELS' else 'NOT_APPLICABLE'}


def inventory_sources(intake):
    """Header-only discovery: every image in each declared folder, no silent role/index selection."""
    from .intake import local_directory
    selection = intake['selection']
    profile = source_profile(selection)
    directories = [selection['masterDirectory']] + profile.get('additionalDirectories', [])
    output, resolved, total = [], set(), 0
    for declared in directories:
        directory = Path(local_directory(declared)).resolve(strict=True)
        local_directory(str(directory))
        require(directory.is_dir() and directory not in resolved, 'MASTER_DIRECTORY_MISSING_OR_DUPLICATE')
        resolved.add(directory)
        files = sorted(p for p in directory.iterdir() if p.is_file() and p.suffix.lower() == '.xisf')
        total += len(files)
        require(total <= 128, 'SOURCE_INVENTORY_FILE_LIMIT')
        for path in files:
            require(not path.is_symlink() and not path.is_junction() and path.resolve(strict=True).parent == directory,
                    'MASTER_OUTSIDE_SELECTED_DIRECTORY')
            with path.open('rb') as stream:
                require(stream.read(8) == b'XISF0100', 'MASTER_XISF')
                header = stream.read(8)
                require(len(header) == 8, 'MASTER_HEADER')
                length, reserved = struct.unpack('<II',header)
                require(0 < length <= 4*1024*1024 and reserved == 0, 'MASTER_HEADER_LIMIT')
                raw = stream.read(length)
            require(len(raw) == length and b'<!DOCTYPE' not in raw and b'<!ENTITY' not in raw, 'MASTER_HEADER')
            images = [e for e in ET.fromstring(raw) if e.tag.split('}')[-1] == 'Image']
            require(1 <= len(images) <= 16, 'MASTER_IMAGES')
            descriptors = []
            for index,image in enumerate(images):
                keywords = {e.get('name'):e.get('value') for e in image if e.tag.split('}')[-1] == 'FITSKeyword' and
                            e.get('name') in {'FILTER','IMAGETYP','BAYERPAT'}}
                descriptors.append({'imageIndex':index,'id':image.get('id'), 'geometry':image.get('geometry'),
                                    'sampleFormat':image.get('sampleFormat'),'colorSpace':image.get('colorSpace'),
                                    'keywords':keywords,'hasAstrometricProperties':any(e.tag.split('}')[-1] == 'Property' and
                                    e.get('id','').startswith('PCL:AstrometricSolution:') for e in image)})
            name = path.name.lower()
            category = 'CALIBRATION' if 'masterbias' in name or 'masterdark' in name or 'masterflat' in name else \
                       'NORMALIZATION_REFERENCE' if name.startswith('ln_reference') else \
                       'DRIZZLE_CANDIDATE' if 'drizzle' in name else 'MASTER_LIGHT_CANDIDATE' if 'masterlight' in name else 'UNCLASSIFIED'
            output.append({'directory':directory.as_posix(),'filename':path.name,'byteSize':path.stat().st_size,
                           'filenameCategory':category,'images':descriptors})
    return {'profile':profile,'files':output,'selection':'EXPLICIT_SELECTION_REQUIRED',
            'authority':'PLANNING_ONLY','linearity':'NATIVE_REVIEW_REQUIRED','registration':'NATIVE_REVIEW_REQUIRED'}
