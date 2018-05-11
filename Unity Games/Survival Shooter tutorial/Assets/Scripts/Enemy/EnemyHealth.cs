using UnityEngine;

public class EnemyHealth : MonoBehaviour
{
    public int startingHealth = 100;
    public int currentHealth;
    public float sinkSpeed = 2.5f;    //pra animacao da morte!
    public int scoreValue = 10;
    public AudioClip deathClip;


    Animator anim;
    AudioSource enemyAudio;
    ParticleSystem hitParticles;
    CapsuleCollider capsuleCollider;
    bool isDead;
    bool isSinking;


    void Awake ()
    {
        anim = GetComponent <Animator> ();
        enemyAudio = GetComponent <AudioSource> ();
        hitParticles = GetComponentInChildren <ParticleSystem> ();//pega a primeira animaçao de particulas que encontra no 
        capsuleCollider = GetComponent <CapsuleCollider> ();

        currentHealth = startingHealth;
    }


    void Update ()
    {
        if(isSinking)
        {
            transform.Translate (-Vector3.up * sinkSpeed * Time.deltaTime);
        }
    }


    public void TakeDamage (int amount, Vector3 hitPoint)
    {
        if(isDead)
            return;

        enemyAudio.Play ();

        currentHealth -= amount;
           
        //ta bugando, dando erro quando atinge outros inimigos al´´em do zumbunny
        //hitParticles.transform.position = hitPoint;
        //hitParticles.Play();

        if(currentHealth <= 0)
        {
            Death ();
        }
    }


    void Death ()
    {
        isDead = true;

        //pode atravessar o inimigo quando ele morre 
        capsuleCollider.isTrigger = true;

        anim.SetTrigger ("Dead");

        enemyAudio.clip = deathClip;
        enemyAudio.Play ();
    }

    //é uma animacao chamada por fora. Ir em models, characters, zombunny e ver na animacao death e clicar em "events" da animacao death. Vai estar ali :3
    public void StartSinking ()
    {
        //desliga o componente 
        GetComponent <UnityEngine.AI.NavMeshAgent> ().enabled = false;

        GetComponent <Rigidbody> ().isKinematic = true;
        isSinking = true;

        //nao precisa abrir um objeto. Usando uma variável estática é mais facil, e como vamos ter varios inimigos, precisa ter apenas UM score. 
        ScoreManager.score += scoreValue;

        Destroy (gameObject, 2f);
    }
}
