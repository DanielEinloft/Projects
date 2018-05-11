using UnityEngine;

// este script utiliza PARTE do prefab do tiro. É copiado um componente do prefab e é colocado no GunBarrelEnd do player
public class PlayerShooting : MonoBehaviour
{
    public int damagePerShot = 20;
    public float timeBetweenBullets = 0.15f;
    public float range = 100f;


    float timer;
    Ray shootRay = new Ray();
    RaycastHit shootHit;
    int shootableMask;
    ParticleSystem gunParticles;
    LineRenderer gunLine;
    AudioSource gunAudio;
    Light gunLight;
    float effectsDisplayTime = 0.2f;


    void Awake ()
    {
        shootableMask = LayerMask.GetMask ("Shootable"); //tudo que é acertável :3 
        gunParticles = GetComponent<ParticleSystem> ();
        gunLine = GetComponent <LineRenderer> ();

        gunLine.startWidth = 0.05f;
        gunLine.endWidth = 0.05f;

        gunAudio = GetComponent<AudioSource> ();
        gunLight = GetComponent<Light> ();
    }


    void Update ()
    {
        timer += Time.deltaTime;

        //fire1 -> botao do mouse :) acho que é o botão esquerdo.
		if(Input.GetButton ("Fire1") && timer >= timeBetweenBullets && Time.timeScale != 0)
        {
            Shoot ();
        }

        if(timer >= timeBetweenBullets * effectsDisplayTime)
        {
            DisableEffects ();
        }
    }


    public void DisableEffects ()
    {
        gunLine.enabled = false;
        gunLight.enabled = false;
    }


    void Shoot ()
    {
        timer = 0f;

        gunAudio.Play ();

        gunLight.enabled = true;

        //força a parada de outra particula pode estar tocando para recomeçar o tiro
        gunParticles.Stop ();
        gunParticles.Play ();


        gunLine.enabled = true;
        // começo da arma, posicao do pai. 
        gunLine.SetPosition (0, transform.position);

        // começa da posicao da arma até a direcao do player.
        shootRay.origin = transform.position;
        shootRay.direction = transform.forward;

        // cria uma classe anônima que realiza um tiro com os parametros configurados.
        if(Physics.Raycast (shootRay, out shootHit, range, shootableMask))
        {
            //se acertar algo..

            //pega a vida de o que atirou.
            EnemyHealth enemyHealth = shootHit.collider.GetComponent <EnemyHealth> ();
            
            //se acertar algo..
            if (enemyHealth != null)
            {
                //toma, desgraça
                enemyHealth.TakeDamage (damagePerShot, shootHit.point);
            }

            // para a linha até o ponto atingido.
            gunLine.SetPosition (1, shootHit.point);
        }
        else
        {
            //caso nao tenha acertado nada, ele vai desenhar uma linha da origem + direçao do tiro * a distância máxima
            gunLine.SetPosition (1, shootRay.origin + shootRay.direction * range);
        }
    }
}
