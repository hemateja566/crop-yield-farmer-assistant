from typing import List, Dict, Any, Optional
from datetime import datetime


class AdvisoryService:
    """Service for generating agricultural advice based on farm data."""
    
    def __init__(self):
        self.knowledge_base = self._load_knowledge_base()
    
    def _load_knowledge_base(self) -> Dict[str, Any]:
        """Load agronomy knowledge base - in production, this would be loaded from documents."""
        return {
            "crops": {
                "rice": {
                    "growth_stages": ["germination", "vegetative", "tillering", "panicle initiation", "flowering", "grain filling", "maturity"],
                    "nutrient_requirements": {
                        "nitrogen": "120-150 kg/ha",
                        "phosphorus": "40-60 kg/ha", 
                        "potassium": "40-50 kg/ha",
                    },
                    "irrigation": "Maintain saturated soil during panicle initiation and flowering",
                    "pest_risks": ["stem borer", "leaf roller", "leaf blight"],
                },
                "wheat": {
                    "growth_stages": ["sowing", "tillering", "stem elongation", "heading", "flowering", "grain filling", "maturity"],
                    "nutrient_requirements": {
                        "nitrogen": "100-130 kg/ha",
                        "phosphorus": "30-40 kg/ha",
                        "potassium": "30-40 kg/ha",
                    },
                    "irrigation": "Irrigate at crown root initiation and flowering if rainfall insufficient",
                    "pest_risks": ["rust", "smut", "aphids"],
                },
            },
            "fertilizer_recommendations": {
                "general": {
                    "basal": "Apply 50% N, 100% P2O5, 100% K2O at planting",
                    "topdress": "Apply remaining 50% N at tillering stage",
                }
            },
            "irrigation_practices": {
                "rice": "Alternate wetting and drying (AWD) can save 15-30% water",
                "wheat": "Irrigation at 30% available soil moisture depletion is optimal",
            },
            "government_guidelines": [
                "Follow local extension service recommendations",
                "Use soil test-based fertilizer application",
                "Adopt integrated pest management (IPM) practices",
            ],
        }
    
    def get_crop_info(self, crop_type: str) -> Optional[Dict[str, Any]]:
        """Get crop-specific cultivation information."""
        crop_type = crop_type.lower()
        return self.knowledge_base["crops"].get(crop_type)
    
    def get_fertilizer_recommendation(self, crop_type: str, soil_nutrients: Dict[str, float]) -> str:
        """Generate fertilizer recommendation based on crop and soil nutrients."""
        crop_info = self.get_crop_info(crop_type)
        if not crop_info:
            return "Consult local agricultural officer for fertilizer recommendations."
        
        n_req = crop_info["nutrient_requirements"].get("nitrogen", "120 kg/ha")
        p_req = crop_info["nutrient_requirements"].get("phosphorus", "40 kg/ha")
        k_req = crop_info["nutrient_requirements"].get("potassium", "40 kg/ha")
        
        n_current = soil_nutrients.get("nitrogen", 0)
        p_current = soil_nutrients.get("phosphorus", 0)
        k_current = soil_nutrients.get("potassium", 0)
        
        recommendation = f"Fertilizer requirements for {crop_type}:\n"
        recommendation += f"• Nitrogen (N): {n_req} (soil: {n_current} units)\n"
        recommendation += f"• Phosphorus (P): {p_req} (soil: {p_current} units)\n"
        recommendation += f"• Potassium (K): {k_req} (soil: {k_current} units)\n"
        
        if crop_info.get("irrigation"):
            recommendation += f"• Irrigation: {crop_info['irrigation']}\n"
        
        if crop_info.get("pest_risks"):
            recommendation += f"• Monitor for: {', '.join(crop_info['pest_risks'])}\n"
        
        return recommendation
    
    def get_irrigation_advice(self, crop_type: str) -> str:
        """Get irrigation advice for a specific crop."""
        crop_info = self.get_crop_info(crop_type)
        if not crop_info or "irrigation" not in crop_info:
            return "Consult local water management guidelines."
        return crop_info["irrigation"]
    
    def get_pest_disease_advice(self, crop_type: str) -> str:
        """Get pest and disease advice for a specific crop."""
        crop_info = self.get_crop_info(crop_type)
        if not crop_info or "pest_risks" not in crop_info:
            return "Regular monitoring recommended. Consult local agricultural extension."
        return f"Monitor for: {', '.join(crop_info['pest_risks'])}"
    
    def get_government_guidelines(self) -> List[str]:
        """Get government agricultural guidelines."""
        return self.knowledge_base.get("government_guidelines", [])