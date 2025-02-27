### Défi de Refactorisation du Suivi d'Astéroïdes NASA

**Contexte:**
Vous avez hérité d'une application Django qui récupère des données d'astéroïdes depuis l'API de la NASA. Le code fonctionne mais nécessite une refactorisation et de nouvelles fonctionnalités.


**Limite de temps:** 3 jours

**Tâches requises:**

1. **Refactorisation du code**
   - Réduire la duplication de code en proposant une/plusieurs refactorisations appropriée
   - Séparer en plusieurs fichiers / controllers
   - Mettre en œuvre une séparation appropriée des préoccupations / de la logique
   - Corriger la gestion des erreurs pour qu'elle soit cohérente et informative

2. **Implémentation de fonctionnalités**
   - **Filtrage**: Ajoutez la possibilité de filtrer les astéroïdes
   - **Améliorer le temps de chargement**
   - **Améliorations du détail de l'astéroide**: afficher les 5 dernières fois ou l'astéroïde est passé proche de la Terre, avec sa date et la distance à laquelle il est passé.

3. **Tests**
   - Ajoutez des tests unitaires pour les nouvelles fonctionnalités

**Notes:**
- Pour les parties 2, 3, libre à vous de proposer des améliorations supplémentaires, UX/UI, en termes de performances, sécurité, etc.
- Pour la contrainte de temps, si vous voulez prendre plus de temps pour une tâche, n'hésitez pas à le faire, signalez-le simplement dans votre PR.
- Partie Frontend est bonus, libre à vous d'utiliser le framework de votre choix. Le but du test n'est pas de vous juger sur vos compétences en frontend, mais de voir comment vous gérez la refactorisation (pour info, nous utilisons Alpine, Htmx, Tailwind)

**Soumission:**
- Soumettez une PR avec vos modifications
- Incluez une brève explication de votre approche de refactorisation et de vos choix


**Env file requit**
- Il est nécessaire de créer un fichier `.env` à la racine du projet avec les variables d'environnement présentes dans le fichier `sample.env`
- Pour la clé API de la NASA, vous pouvez en créer une [ici](https://api.nasa.gov/index.html#authentication)
                                                             