import csv
from math import exp, sqrt, log10
from Data.DataExtraction import ensureMammalCSV

class PredatorPreyRelations:
    def __init__(self):
        
        self._relations = {}  # list of (predator, prey) pairs
        self._lv_coeffs = {}

    def addRelation(self, predator, prey, alpha=None):
        #store the predator-prey pair by adding it to internal list of relationships
        

        if predator not in self._relations:
            self._relations[predator] = set()
        self._relations[predator].add(prey)

        if alpha is not None:
            self._lv_coeffs[(predator, prey)] = alpha


    def eat(self, predator, prey):
        # Determine if this predator can eat this prey
        return prey in self._relations.get(predator, set())

    def prey_PredatorCanEat(self, predator):
        # Determine all prey this predator can eat and store as list
        return list(self._relations.get(predator, set()))

    def allPredators_thatCanEatThisPrey(self, prey):
        # List of predators that can eat this prey.
        result = []
        for pred, prey_list in self._relations.items():
            if prey in prey_list:
                result.append(pred)
        return result
    
    def getAlpha(self, predator, prey, default=0.0):
        return self._lv_coeffs.get((predator, prey), default)
    
    def buildRelationsFromData(self,
        mammalCSV,
        alpha_threshold=0.05,
    ):
        
        import math

        def safeFloat(value, fallback=0.0):
            try:
                return float(value)
            except (ValueError, TypeError):
                return fallback

        def classifyEnv(terr_value: float) -> str:
            """
        
            >= 0.75  -> 'land'
            <= 0.25  -> 'water'
            else     -> 'mixed'  (semi-aquatic, etc.)
            """
            if terr_value >= 0.75:
                return "land"
            elif terr_value <= 0.25:
                return "water"
            else:
                return "mixed"

        #load rows and compute habitat 
        rows = []
        with open(mammalCSV, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                terr = safeFloat(row.get("terrestriality"), 0.0)
                row["_env"] = classifyEnv(terr)
                rows.append(row)

        predators = []
        preyList = []

        #split by trophic level
        for r in rows:
            trophic = safeFloat(r.get("trophic_level"), 0.0)
            if trophic >= 3.0:
                predators.append(r)
            else:
                preyList.append(r)

        # build predator–prey 
        for pred in predators:
            predName = pred.get("species")
            if not predName:
                continue

            predEnv = pred.get("_env", "unknown")
            predMass = safeFloat(pred.get("adult_mass_g"), 0.0)
            predTrophic = safeFloat(pred.get("trophic_level"), 0.0)
            if predMass <= 0:
                continue

            for prey in preyList:
                preyName = prey.get("species")
                if not preyName or preyName == predName:
                    continue

                preyEnv = prey.get("_env", "unknown")

                # habitat filler
                # Only allow pairs that share a habitat,
                # unless one of them is mixed 
                if (predEnv != preyEnv
                    and predEnv != "mixed"
                    and preyEnv != "mixed"):
                    continue

                preyMass = safeFloat(prey.get("adult_mass_g"), 0.0)
                preyTrophic = safeFloat(prey.get("trophic_level"), 0.0)
                if preyMass <= 0:
                    continue

                # trophic difference: predator must be higher
                trophicDiff = max(predTrophic - preyTrophic, 0.0)
                if trophicDiff <= 0:
                    continue

                # size_factor: in (0, 1), larger if predator >> prey
                sizeFactor = predMass / (predMass + preyMass)

                
                ratio = max(predMass / preyMass, 1e-6)
                overlapFactor = math.exp(-abs(math.log(ratio)))

                # Lotka–Volterra interaction coefficient
                alpha_ij = trophicDiff * sizeFactor * overlapFactor

                if alpha_ij >= alpha_threshold:
                    self.addRelation(predName, preyName, alpha=alpha_ij)

        return self._relations


    def removeSpecies(self, species):
        """
        Remove a species from the relationships:
        -Predator as the key
        -as a prey (value) under all predators
        """
        # Remove as predator
        if species in self._relations:
            del self._relations[species]

        # Remove as prey from all predators
        for pred in list(self._relations.keys()):
            prey_set = self._relations[pred]
            if species in prey_set:
                prey_set.remove(species)
            # drop predators that end up with no prey
            if not prey_set:
                del self._relations[pred]

def buildRelationsFromMammalData(alphaThreshold=0.05):
    """
    1. Ensure mammalAnimals.csv exists.
    2. Build PredatorPreyRelations from that CSV.
    3. Return the PredatorPreyRelations instance.
    """
    csvPath = ensureMammalCSV()
    rel = PredatorPreyRelations()
    rel.buildRelationsFromData(csvPath, alphaThreshold=alphaThreshold)
    return rel


from math import sqrt

def compareBehaviorToDataset(simulationBehavior, datasetRows):
        
    def safeFloat(value, default=0.0):
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
            
    def predatoRow(row):
        t = safeFloat(row.get("trophic_level"))
        return t >= 3.0

    def preyRow(row):
        t = safeFloat(row.get("trophic_level"))
        return 0 < t < 3.0

    simType = simulationBehavior.get("type")
    simMass = safeFloat(simulationBehavior.get("size", 0.0))
    simRepro = safeFloat(simulationBehavior.get("reproductionRate", 0.0))

    # Step 1: filter by trophic_level based on type
    candidates = []
    for row in datasetRows:
        if simType == "predator" and not predatoRow(row):
            continue
        if simType == "prey" and not preyRow(row):
            continue
        candidates.append(row)

    # Fallback if trophic filters remove everything
    if not candidates:
        candidates = list(datasetRows)

    # Step 2: filter by weight class (~0.1x to 10x mass)
    if simMass > 0:
        filtered = []
        for row in candidates:
            rowMass = safeFloat(row.get("adult_mass_g"))
            if rowMass <= 0:
                continue
            ratio = rowMass / simMass
            if 0.1 <= ratio <= 10.0:
                filtered.append(row)
        if filtered:
            candidates = filtered

    # Step 3: similarity using log-scaled mass & age at first birth
    def similarity(row):
        rowMass = safeFloat(row.get("adult_mass_g"))
        rowRepro = safeFloat(row.get("age_first_birth_d"))

        log_sim_mass = log10(simMass + 1.0)
        log_row_mass = log10(rowMass + 1.0)

        log_sim_repro = log10(simRepro + 1.0)
        log_row_repro = log10(rowRepro + 1.0)

        return sqrt(
            (log_sim_mass  - log_row_mass)  ** 2 +
            (log_sim_repro - log_row_repro) ** 2
        )

    bestSpecies = None
    bestScore = float("inf")

    for row in candidates:
        d = similarity(row)
        if d < bestScore:
            bestScore = d
            bestSpecies = row.get("species", row.get("species_short", "Unknown"))

    return bestSpecies, bestScore
