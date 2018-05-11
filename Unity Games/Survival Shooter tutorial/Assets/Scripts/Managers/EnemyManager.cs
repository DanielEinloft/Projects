using UnityEngine;

public class EnemyManager : MonoBehaviour
{
    public PlayerHealth playerHealth;
    public GameObject enemy;
    public float spawnTime = 3f;
    public Transform[] spawnPoints;// pode ter varios mas neste caso so uma uma posicao


    void Start ()
    {
        //funcao que vai ficar sendo executada em 3f segundos :O
        InvokeRepeating ("Spawn", spawnTime, spawnTime);
    }


    void Spawn ()
    {
        if(playerHealth.currentHealth <= 0f)
        {
            return;
        }

        //gera aleatoriamente um indice de  0 até o tamanho so spawnpoints. no nosso caso, sempre vai ter um só. Mas isso serve pra no instantiate spawnar em pontos aleatorios pre definidos
        int spawnPointIndex = Random.Range (0, spawnPoints.Length);

        Instantiate (enemy, spawnPoints[spawnPointIndex].position, spawnPoints[spawnPointIndex].rotation);
    }
}
