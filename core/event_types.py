import json
import os
import random
import math
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

@dataclass
class CutLine:
    """Represents cut line configuration for a tournament"""
    type: str  # "position", "score", etc.
    value: int
    description: str

@dataclass
class PointsStructure:
    """Represents points allocation for different finishing positions"""
    winner: int
    runner_up: int
    top_3: int
    top_4: float
    top_5: float
    top_6: float
    top_7: float
    top_8: float
    top_9: float
    top_10: float
    top_11: float
    top_12: float
    top_13: float
    top_14: float
    top_15: float
    top_16: float
    top_17: float
    top_18: float
    top_19: float
    top_20: float
    top_21: float
    top_22: float
    top_23: float
    top_24: float
    top_25: float
    top_26: float
    top_27: float
    top_28: float
    top_29: float
    top_30: float
    top_31: float
    top_32: float
    top_33: float
    top_34: float
    top_35: float
    top_36: float
    top_37: float
    top_38: float
    top_39: float
    top_40: float
    top_41: float
    top_42: float
    top_43: float
    top_44: float
    top_45: float
    top_46: float
    top_47: float
    top_48: float
    top_49: float
    top_50: float
    top_51: float
    top_52: float
    top_53: float
    top_54: float
    top_55: float
    top_56: float
    top_57: float
    top_58: float
    top_59: float
    top_60: float
    top_61: float
    top_62: float
    top_63: float
    top_64: float
    top_65: float
    top_66: float
    top_67: float
    top_68: float
    top_69: float
    top_70: float
    top_71: float
    top_72: float
    top_73: float
    top_74: float
    top_75: float
    top_76: float
    top_77: float
    top_78: float
    top_79: float
    top_80: float
    top_81: float
    top_82: float
    top_83: float
    top_84: float
    top_85: float
    made_cut: float

@dataclass
class EventType:
    """Represents an event type configuration"""
    name: str
    field_size: Any  # Can be int or dict for random
    cut_line: CutLine
    purse_base: Any  # Can be int or dict for random
    points_structure: PointsStructure
    payout_percentages: Dict[str, float]
    prestige: Any  # Can be float or dict for random
    qualification_methods: List[str]
    rounds: int
    description: str

class EventTypeManager:
    """Manages event type configurations and tournament overrides"""
    
    def __init__(self):
        self.config_dir = os.path.join(os.path.dirname(__file__), '..', 'config')
        self.event_types = {}
        self.tournament_overrides = {}
        self._load_configurations()
    
    def _load_configurations(self):
        """Load event type configurations from JSON files"""
        # Load base event types
        event_types_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'event_types.json')
        with open(event_types_path, 'r') as f:
            event_types_data = json.load(f)
        
        for event_type_key, data in event_types_data.items():
            self.event_types[event_type_key] = self._create_event_type(data)
        
        # Load tournament overrides
        overrides_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'tournament_overrides.json')
        with open(overrides_path, 'r') as f:
            overrides_data = json.load(f)
        
        # Load majors
        if 'majors' in overrides_data:
            for tournament_name, override_data in overrides_data['majors'].items():
                self.tournament_overrides[tournament_name] = override_data
        
        # Load special events
        if 'special_events' in overrides_data:
            for tournament_name, override_data in overrides_data['special_events'].items():
                self.tournament_overrides[tournament_name] = override_data
        
        # Load invitationals
        if 'invitationals' in overrides_data:
            for tournament_name, override_data in overrides_data['invitationals'].items():
                self.tournament_overrides[tournament_name] = override_data
    
    def _generate_random_field_size(self, config: Dict[str, Any]) -> int:
        """Generate random field size based on configuration"""
        if isinstance(config, dict) and config.get('type') == 'random':
            min_size = config['min']
            max_size = config['max']
            multiple = config.get('multiple', 1)
            
            # Generate random number between min and max
            random_size = random.randint(min_size, max_size)
            
            # Round to nearest multiple
            if multiple > 1:
                random_size = round(random_size / multiple) * multiple
            
            return random_size
        else:
            return config if isinstance(config, int) else 156
    
    def _generate_random_purse(self, config: Dict[str, Any]) -> int:
        """Generate random purse amount based on configuration"""
        if isinstance(config, dict) and config.get('type') == 'random':
            min_purse = config['min']
            max_purse = config['max']
            round_to = config.get('round_to', 1000)
            
            # Generate random amount
            random_purse = random.randint(min_purse, max_purse)
            
            # Round to specified increment
            if round_to > 1:
                random_purse = round(random_purse / round_to) * round_to
            
            return random_purse
        else:
            return config if isinstance(config, int) else 8500000
    
    def _generate_random_prestige(self, config: Dict[str, Any]) -> float:
        """Generate random prestige level based on configuration"""
        if isinstance(config, dict) and config.get('type') == 'random':
            min_prestige = config['min']
            max_prestige = config['max']
            
            # Generate random float between min and max
            random_prestige = random.uniform(min_prestige, max_prestige)
            
            # Round to 2 decimal places
            return round(random_prestige, 2)
        else:
            return config if isinstance(config, (int, float)) else 3.5
    
    def _create_event_type(self, data: Dict[str, Any]) -> EventType:
        """Create an EventType instance from configuration data"""
        cut_line = CutLine(
            type=data['cut_line']['type'],
            value=data['cut_line']['value'],
            description=data['cut_line']['description']
        )
        
        # Handle points structure - check what positions are actually defined
        points_data = data['points_structure']
        points_structure = PointsStructure(
            winner=points_data.get('winner', 500),
            runner_up=points_data.get('runner_up', 275),
            top_3=points_data.get('top_3', 175),
            top_4=points_data.get('top_4', 133.33),
            top_5=points_data.get('top_5', 108.33),
            top_6=points_data.get('top_6', 100),
            top_7=points_data.get('top_7', 91.67),
            top_8=points_data.get('top_8', 83.33),
            top_9=points_data.get('top_9', 75),
            top_10=points_data.get('top_10', 66.67),
            top_11=points_data.get('top_11', 62.5),
            top_12=points_data.get('top_12', 58.33),
            top_13=points_data.get('top_13', 54.17),
            top_14=points_data.get('top_14', 51.67),
            top_15=points_data.get('top_15', 50.83),
            top_16=points_data.get('top_16', 50),
            top_17=points_data.get('top_17', 49.17),
            top_18=points_data.get('top_18', 48.33),
            top_19=points_data.get('top_19', 47.5),
            top_20=points_data.get('top_20', 46.67),
            top_21=points_data.get('top_21', 44.6),
            top_22=points_data.get('top_22', 42.52),
            top_23=points_data.get('top_23', 40.45),
            top_24=points_data.get('top_24', 38.37),
            top_25=points_data.get('top_25', 36.82),
            top_26=points_data.get('top_26', 35.27),
            top_27=points_data.get('top_27', 33.7),
            top_28=points_data.get('top_28', 32.15),
            top_29=points_data.get('top_29', 30.6),
            top_30=points_data.get('top_30', 29.03),
            top_31=points_data.get('top_31', 27.48),
            top_32=points_data.get('top_32', 25.93),
            top_33=points_data.get('top_33', 24.37),
            top_34=points_data.get('top_34', 22.82),
            top_35=points_data.get('top_35', 21.78),
            top_36=points_data.get('top_36', 20.73),
            top_37=points_data.get('top_37', 19.7),
            top_38=points_data.get('top_38', 18.67),
            top_39=points_data.get('top_39', 17.63),
            top_40=points_data.get('top_40', 16.6),
            top_41=points_data.get('top_41', 15.55),
            top_42=points_data.get('top_42', 14.52),
            top_43=points_data.get('top_43', 13.48),
            top_44=points_data.get('top_44', 12.45),
            top_45=points_data.get('top_45', 11.4),
            top_46=points_data.get('top_46', 10.88),
            top_47=points_data.get('top_47', 10.37),
            top_48=points_data.get('top_48', 9.85),
            top_49=points_data.get('top_49', 9.33),
            top_50=points_data.get('top_50', 8.82),
            top_51=points_data.get('top_51', 8.3),
            top_52=points_data.get('top_52', 7.78),
            top_53=points_data.get('top_53', 7.27),
            top_54=points_data.get('top_54', 6.73),
            top_55=points_data.get('top_55', 6.22),
            top_56=points_data.get('top_56', 6.02),
            top_57=points_data.get('top_57', 5.8),
            top_58=points_data.get('top_58', 5.6),
            top_59=points_data.get('top_59', 5.4),
            top_60=points_data.get('top_60', 5.18),
            top_61=points_data.get('top_61', 4.98),
            top_62=points_data.get('top_62', 4.77),
            top_63=points_data.get('top_63', 4.57),
            top_64=points_data.get('top_64', 4.35),
            top_65=points_data.get('top_65', 4.15),
            top_66=points_data.get('top_66', 3.93),
            top_67=points_data.get('top_67', 3.73),
            top_68=points_data.get('top_68', 3.53),
            top_69=points_data.get('top_69', 3.32),
            top_70=points_data.get('top_70', 3.12),
            top_71=points_data.get('top_71', 3),
            top_72=points_data.get('top_72', 2.9),
            top_73=points_data.get('top_73', 2.8),
            top_74=points_data.get('top_74', 2.7),
            top_75=points_data.get('top_75', 2.6),
            top_76=points_data.get('top_76', 2.48),
            top_77=points_data.get('top_77', 2.38),
            top_78=points_data.get('top_78', 2.28),
            top_79=points_data.get('top_79', 2.18),
            top_80=points_data.get('top_80', 2.07),
            top_81=points_data.get('top_81', 1.97),
            top_82=points_data.get('top_82', 1.87),
            top_83=points_data.get('top_83', 1.77),
            top_84=points_data.get('top_84', 1.67),
            top_85=points_data.get('top_85', 1.55),
            made_cut=points_data.get('made_cut', 1.55)
        )
        
        return EventType(
            name=data['name'],
            field_size=data['field_size'],
            cut_line=cut_line,
            purse_base=data['purse_base'],
            points_structure=points_structure,
            payout_percentages={},  # Empty dict since we use dynamic payouts
            prestige=data['prestige'],
            qualification_methods=data['qualification_methods'],
            rounds=data['rounds'],
            description=data['description']
        )
    
    def get_event_type(self, event_type_key: str) -> Optional[EventType]:
        """Get an event type by key"""
        return self.event_types.get(event_type_key)
    
    def get_tournament_config(self, tournament_name: str) -> Dict[str, Any]:
        """Get tournament configuration with overrides applied and random values generated"""
        # Check if tournament has specific overrides
        if tournament_name in self.tournament_overrides:
            override = self.tournament_overrides[tournament_name]
            event_type_key = override['event_type']
            base_config = self.event_types[event_type_key]
            
            # Apply overrides or generate random values
            # Handle field_size override (check both field_size_override and field_size)
            field_size = override.get('field_size_override') or override.get('field_size')
            if field_size is None:
                field_size = self._generate_random_field_size(base_config.field_size)
            elif isinstance(field_size, dict):
                field_size = self._generate_random_field_size(field_size)
            
            # Handle purse override (check both purse_override and purse_base)
            purse_base = override.get('purse_override') or override.get('purse_base')
            if purse_base is None:
                purse_base = self._generate_random_purse(base_config.purse_base)
            elif isinstance(purse_base, dict):
                if purse_base.get('type') == 'fixed':
                    purse_base = purse_base['value']
                else:
                    purse_base = self._generate_random_purse(purse_base)
            
            # Handle prestige override
            prestige = override.get('prestige_override') or override.get('prestige')
            if prestige is None:
                prestige = self._generate_random_prestige(base_config.prestige)
            elif isinstance(prestige, dict):
                if prestige.get('type') == 'fixed':
                    prestige = prestige['value']
                else:
                    prestige = self._generate_random_prestige(prestige)
            
            # Handle cut line override
            cut_line = override.get('cut_line_override') or override.get('cut_line')
            if cut_line is None:
                cut_line = {
                    'type': base_config.cut_line.type,
                    'value': base_config.cut_line.value,
                    'description': base_config.cut_line.description
                }
            
            # Handle qualification methods override
            qualification_methods = override.get('qualification_methods', base_config.qualification_methods)
            
            # Handle points structure override
            points_structure = override.get('points_structure', self._get_points_structure_dict(base_config.points_structure))
            
            # Handle payout percentages override
            payout_percentages = override.get('payout_percentages', base_config.payout_percentages)
            
            # Create merged configuration
            config = {
                'event_type': event_type_key,
                'name': base_config.name,
                'field_size': field_size,
                'cut_line': cut_line,
                'purse_base': purse_base,
                'points_structure': points_structure,
                'payout_percentages': payout_percentages,
                'prestige': prestige,
                'qualification_methods': qualification_methods,
                'rounds': base_config.rounds,
                'description': override.get('description', base_config.description)
            }
        else:
            # Check if this is a custom major from the "majors" section
            custom_majors = self.tournament_overrides.get('majors', {})
            if tournament_name in custom_majors:
                major_config = custom_majors[tournament_name]
                base_config = self.event_types['major']
                
                # Use custom major configuration
                field_size = major_config.get('field_size', 156)
                if isinstance(field_size, dict):
                    field_size = self._generate_random_field_size(field_size)
                
                purse_base = major_config.get('purse_base', 20000000)
                if isinstance(purse_base, dict):
                    purse_base = self._generate_random_purse(purse_base)
                
                prestige = major_config.get('prestige', 9.5)
                if isinstance(prestige, dict):
                    prestige = self._generate_random_prestige(prestige)
                
                cut_line = major_config.get('cut_line', {
                    'type': 'position',
                    'value': 70,
                    'description': 'Top 70 and ties advance to weekend'
                })
                
                qualification_methods = major_config.get('qualification_methods', [
                    'world_rank_top_50',
                    'past_champions',
                    'fedex_rank_top_30',
                    'special_invitation'
                ])
                
                points_structure = major_config.get('points_structure', self._get_points_structure_dict(base_config.points_structure))
                payout_percentages = major_config.get('payout_percentages', base_config.payout_percentages)
                
                config = {
                    'event_type': 'major',
                    'name': base_config.name,
                    'field_size': field_size,
                    'cut_line': cut_line,
                    'purse_base': purse_base,
                    'points_structure': points_structure,
                    'payout_percentages': payout_percentages,
                    'prestige': prestige,
                    'qualification_methods': qualification_methods,
                    'rounds': base_config.rounds,
                    'description': major_config.get('description', base_config.description)
                }
            else:
                # Determine event type from tournament name or use standard
                event_type_key = self._determine_event_type_from_name(tournament_name)
                base_config = self.event_types[event_type_key]
                
                # For majors, use better default values if no specific override exists
                if event_type_key == 'major':
                    # Use more realistic major defaults
                    field_size = 156  # Standard major field size
                    purse_base = 20000000  # $20M default purse for majors
                    prestige = 9.5  # High prestige for majors
                    cut_line = {
                        'type': 'position',
                        'value': 70,
                        'description': 'Top 70 and ties advance to weekend'
                    }
                    qualification_methods = [
                        'world_rank_top_50',
                        'past_champions',
                        'fedex_rank_top_30',
                        'special_invitation'
                    ]
                else:
                    # Generate random values for this tournament
                    field_size = self._generate_random_field_size(base_config.field_size)
                    purse_base = self._generate_random_purse(base_config.purse_base)
                    prestige = self._generate_random_prestige(base_config.prestige)
                    cut_line = {
                        'type': base_config.cut_line.type,
                        'value': base_config.cut_line.value,
                        'description': base_config.cut_line.description
                    }
                    qualification_methods = base_config.qualification_methods
                
                config = {
                    'event_type': event_type_key,
                    'name': base_config.name,
                    'field_size': field_size,
                    'cut_line': cut_line,
                    'purse_base': purse_base,
                    'points_structure': self._get_points_structure_dict(base_config.points_structure),
                    'payout_percentages': base_config.payout_percentages,
                    'prestige': prestige,
                    'qualification_methods': qualification_methods,
                    'rounds': base_config.rounds,
                    'description': base_config.description
                }
        
        return config
    
    def _determine_event_type_from_name(self, tournament_name: str) -> str:
        """Determine event type from tournament name"""
        name_lower = tournament_name.lower()
        
        # Check for major championships - expanded list
        major_keywords = [
            'sovereign tournament', 'aga championship', 'american open championship', 
            'royal open championship', 'masters', 'pga championship', 'u.s. open', 
            'the open championship', 'open championship', 'major', 'championship'
        ]
        for keyword in major_keywords:
            if keyword in name_lower:
                return 'major'
        
        # Check for invitationals
        invitational_keywords = ['invitational', 'memorial', 'arnold palmer', 'players championship']
        for keyword in invitational_keywords:
            if keyword in name_lower:
                return 'invitational'
        
        # Check for opens (but not major championships)
        open_keywords = ['open']
        for keyword in open_keywords:
            if keyword in name_lower and 'championship' not in name_lower:
                # PATCH: Never return 'open' as an event type, treat as standard
                return 'standard'
        
        # Default to standard
        return 'standard'
    
    def _get_points_structure_dict(self, points_structure: PointsStructure) -> Dict[str, Any]:
        """Convert PointsStructure to dictionary format"""
        return {
            'winner': points_structure.winner,
            'runner_up': points_structure.runner_up,
            'top_3': points_structure.top_3,
            'top_4': points_structure.top_4,
            'top_5': points_structure.top_5,
            'top_6': points_structure.top_6,
            'top_7': points_structure.top_7,
            'top_8': points_structure.top_8,
            'top_9': points_structure.top_9,
            'top_10': points_structure.top_10,
            'top_11': points_structure.top_11,
            'top_12': points_structure.top_12,
            'top_13': points_structure.top_13,
            'top_14': points_structure.top_14,
            'top_15': points_structure.top_15,
            'top_16': points_structure.top_16,
            'top_17': points_structure.top_17,
            'top_18': points_structure.top_18,
            'top_19': points_structure.top_19,
            'top_20': points_structure.top_20,
            'top_21': points_structure.top_21,
            'top_22': points_structure.top_22,
            'top_23': points_structure.top_23,
            'top_24': points_structure.top_24,
            'top_25': points_structure.top_25,
            'top_26': points_structure.top_26,
            'top_27': points_structure.top_27,
            'top_28': points_structure.top_28,
            'top_29': points_structure.top_29,
            'top_30': points_structure.top_30,
            'top_31': points_structure.top_31,
            'top_32': points_structure.top_32,
            'top_33': points_structure.top_33,
            'top_34': points_structure.top_34,
            'top_35': points_structure.top_35,
            'top_36': points_structure.top_36,
            'top_37': points_structure.top_37,
            'top_38': points_structure.top_38,
            'top_39': points_structure.top_39,
            'top_40': points_structure.top_40,
            'top_41': points_structure.top_41,
            'top_42': points_structure.top_42,
            'top_43': points_structure.top_43,
            'top_44': points_structure.top_44,
            'top_45': points_structure.top_45,
            'top_46': points_structure.top_46,
            'top_47': points_structure.top_47,
            'top_48': points_structure.top_48,
            'top_49': points_structure.top_49,
            'top_50': points_structure.top_50,
            'top_51': points_structure.top_51,
            'top_52': points_structure.top_52,
            'top_53': points_structure.top_53,
            'top_54': points_structure.top_54,
            'top_55': points_structure.top_55,
            'top_56': points_structure.top_56,
            'top_57': points_structure.top_57,
            'top_58': points_structure.top_58,
            'top_59': points_structure.top_59,
            'top_60': points_structure.top_60,
            'top_61': points_structure.top_61,
            'top_62': points_structure.top_62,
            'top_63': points_structure.top_63,
            'top_64': points_structure.top_64,
            'top_65': points_structure.top_65,
            'top_66': points_structure.top_66,
            'top_67': points_structure.top_67,
            'top_68': points_structure.top_68,
            'top_69': points_structure.top_69,
            'top_70': points_structure.top_70,
            'top_71': points_structure.top_71,
            'top_72': points_structure.top_72,
            'top_73': points_structure.top_73,
            'top_74': points_structure.top_74,
            'top_75': points_structure.top_75,
            'top_76': points_structure.top_76,
            'top_77': points_structure.top_77,
            'top_78': points_structure.top_78,
            'top_79': points_structure.top_79,
            'top_80': points_structure.top_80,
            'top_81': points_structure.top_81,
            'top_82': points_structure.top_82,
            'top_83': points_structure.top_83,
            'top_84': points_structure.top_84,
            'top_85': points_structure.top_85,
            'made_cut': points_structure.made_cut
        }
    
    def get_points_for_position(self, tournament_name: str, position: int) -> float:
        """Get points awarded for a specific finishing position"""
        config = self.get_tournament_config(tournament_name)
        points_structure = config['points_structure']
        event_type = config['event_type']
        
        # Handle majors and standard events with detailed points structure
        if event_type in ['major', 'standard'] and 'top_4' in points_structure and points_structure['top_4'] > 0:
            # Detailed points structure (majors and standard events)
            if position == 1:
                return points_structure['winner']
            elif position == 2:
                return points_structure['runner_up']
            elif position == 3:
                return points_structure['top_3']
            elif position <= 85:
                # Get the specific position points
                position_key = f'top_{position}'
                if position_key in points_structure:
                    return points_structure[position_key]
                else:
                    return points_structure['made_cut']
            else:
                return points_structure['made_cut']
        else:
            # Simple points structure (invitationals and other event types)
            if position == 1:
                return points_structure['winner']
            elif position == 2:
                return points_structure['runner_up']
            elif position <= 3:
                return points_structure['top_3']
            elif position <= 5:
                return points_structure['top_5']
            elif position <= 10:
                return points_structure['top_10']
            elif position <= 20:
                return points_structure['top_20']
            elif position <= 30:
                return points_structure['top_30']
            else:
                return points_structure['made_cut']
    
    def list_event_types(self) -> List[str]:
        """List all available event types"""
        return list(self.event_types.keys())
    
    def list_tournament_overrides(self) -> List[str]:
        """List all tournaments with specific overrides"""
        return list(self.tournament_overrides.keys())

# Global instance for easy access
event_type_manager = EventTypeManager() 