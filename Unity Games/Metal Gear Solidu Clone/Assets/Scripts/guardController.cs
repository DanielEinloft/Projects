using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class guardController : MonoBehaviour
{
    [Header("Game Objects")]
    public Transform guardPath;
    public Transform player;
    public LayerMask Obstacle;
    public GameObject bulletPrefab;
    public Transform otherGuards;




    [Header("Controle Variables")]
    public float guardSpeed;
    public float turnSpeed;
    public float spotDistance;
    public bool playerSpotted;
    public float fieldOfView;
    public float life;
    public float projectileForce = 500f;


    Vector3 LastPath;
    float LastViewAngle;
    NavMeshAgent navMesh;
    float shotDelay;
    bool playerSpottedBuffer = false;



    //Methods:
    void Start()
    {
        guardSpeed = 10f;
        turnSpeed = 180;
        spotDistance = 30;
        playerSpotted = false;
        fieldOfView = 90;
        LastPath = new Vector3(0, 0, 0);
        LastViewAngle = 0f;
        life = 2;


        navMesh = this.GetComponent<NavMeshAgent>();
        navMesh.speed = guardSpeed;
        //navMesh.height = 0.5f;
        //navMesh.baseOffset = 0;
        navMesh.angularSpeed = turnSpeed;
        shotDelay = 0f;


        StartCoroutine(followPath());
    }

    IEnumerator smoothLookAtWaypoint(Vector3 waypoint)
    {

        Vector3 directionNormalized = ((waypoint - transform.position).normalized);
        float angle = 90 - Mathf.Atan2(directionNormalized.z, directionNormalized.x) * Mathf.Rad2Deg; //90 -> no rotation => z axis

        //absolute angle between 2 points. % 360 to restart when angle > 360
        while ((Mathf.Abs(transform.eulerAngles.y - angle) % 360) > 0.05f)
        {
            //if (playerSpotted)
            //    yield return followPlayer();

            float angleBuff = Mathf.MoveTowardsAngle(transform.eulerAngles.y, angle, turnSpeed * Time.deltaTime);
            transform.eulerAngles = new Vector3(0, angleBuff, 0);
            yield return null;
        }

    }
    IEnumerator followPlayer(int nextPath)
    {
        navMesh.enabled = true;
        float time = Time.time;

        if (player != null)
        {
            while (true)
            {
                if (player != null)
                {
                    if (!Physics.Linecast(transform.position, player.position, Obstacle) && playerSpotted)
                    {
                        navMesh.enabled = true;
                        navMesh.SetDestination(player.position);
                        time = Time.time;

                    }
                    else
                    {

                        if (Time.time - time > 2f)
                        {
                            playerSpottedBuffer = false;
                            navMesh.SetDestination(new Vector3(LastPath.x, transform.position.y, LastPath.z));
                            if (Mathf.Abs(new Vector3(transform.position.x - LastPath.x, 0, transform.position.z - LastPath.z).magnitude) < 1f)
                            {
                                navMesh.enabled = false;
                                yield return smoothLookAtWaypoint(guardPath.GetChild(nextPath).position);
                                break;
                            }
                        }
                        else
                        {
                            navMesh.enabled = true;
                            navMesh.SetDestination(player.position);
                        }

                    }
                }
                else
                {
                    playerSpottedBuffer = false;
                    yield return smoothLookAtWaypoint(guardPath.GetChild(nextPath).position);
                    navMesh.SetDestination(new Vector3(LastPath.x, transform.position.y, LastPath.z));
                    if (Mathf.Abs(new Vector3(transform.position.x - LastPath.x, 0, transform.position.z - LastPath.z).magnitude) < 1f)
                    {
                        navMesh.enabled = false;
                        yield return smoothLookAtWaypoint(guardPath.GetChild(nextPath).position);
                        break;
                    }
                    //break; //se der bosta descomentar isso
                }
                yield return null;

            }
        }


    }
    IEnumerator followPath()
    {
        while (true)
        {
            //transform.position = Vector3.MoveTowards(transform.position, guardPath.GetChild(0).position, guardSpeed * Time.deltaTime);
            for (int i = 0; i < guardPath.childCount; i++)
            {
                //use yield return to each function you want to call.
                yield return smoothLookAtWaypoint(guardPath.GetChild(i).position);
                LastViewAngle = transform.eulerAngles.y;


                //if (playerSpotted)
                //    yield return followPlayer(i);
                navMesh.enabled = false;
                //while (transform.position.x != guardPath.GetChild(i).position.x && transform.position.z != guardPath.GetChild(i).position.z)

                while (Mathf.Abs(new Vector3(transform.position.x - guardPath.GetChild(i).position.x, 0, transform.position.z - guardPath.GetChild(i).position.z).magnitude) > 0.5f)
                {
                    //print(Mathf.Abs(new Vector3(transform.position.x - guardPath.GetChild(i).position.x, 0, transform.position.z - guardPath.GetChild(i).position.z).magnitude));
                    //print(transform.position);
                    //Debug.Log(transform.position.z + " " + guardPath.GetChild(i).position.z);
                    //Debug.Log(transform.position.x == guardPath.GetChild(i).position.x );

                    if (playerSpotted)
                    {
                        yield return followPlayer(i);
                        yield return new WaitForSeconds(1f);
                        navMesh.enabled = false;
                    }

                    // print(i + " " + Mathf.Abs(new Vector3(transform.position.x - guardPath.GetChild(i).position.x,0, transform.position.z - guardPath.GetChild(i).position.z).magnitude));

                    LastPath = transform.position;
                    transform.position = Vector3.MoveTowards(transform.position, new Vector3(guardPath.GetChild(i).position.x, transform.position.y, guardPath.GetChild(i).position.z), guardSpeed * Time.deltaTime);
                    yield return null;

                }
                yield return new WaitForSeconds(0.5f);

            }
            yield return null;
        }
    }

    void callGuards()
    {
        for(int i =0;i <otherGuards.childCount;i++)
        {
            otherGuards.GetChild(i).GetComponent<guardController>().someoneFoundPLayer();
        }
    }
    public void someoneFoundPLayer()
    {
        playerSpottedBuffer = true;
    }
    private bool spotPlayer()
    {
        if(player != null)
        {
            Vector3 distanceVector = (player.position - transform.position);
            if (Mathf.Abs(distanceVector.magnitude) <= spotDistance)
            {
                if (Mathf.Abs(Vector3.Angle(transform.forward, distanceVector)) <= fieldOfView / 2f)
                {
                    if (!Physics.Linecast(transform.position, player.position, Obstacle))
                    {
                        if(!player.GetComponent<playerMovement>().isHidden())
                        {
                            callGuards();
                            return true;
                        }
                    }
                }
            }
        }
        return false;
    }
    void OnDrawGizmos()
    {

        Gizmos.DrawSphere(guardPath.GetChild(0).position, 0.5f);

        for ( int i =1; i < guardPath.childCount; i++)
        {
            Gizmos.DrawSphere(guardPath.GetChild(i).position,0.5f);
            Gizmos.DrawLine(guardPath.GetChild(i-1).position, guardPath.GetChild(i).position);

        }
        Gizmos.DrawLine(guardPath.GetChild(guardPath.childCount - 1).position, guardPath.GetChild(0).position);

    }
    public void takeDamage()
    {
        life--;
        if(life == 0)
            Destroy(gameObject);
    }
    void shootAtPlayer()
    {
        if(player != null)
        {
            if (!Physics.Linecast(transform.position, player.position, Obstacle))
            {
                GameObject bullet = (GameObject)Instantiate(bulletPrefab, transform.position + transform.forward * 4, transform.rotation);
                bullet.GetComponent<Rigidbody>().AddForce(transform.forward * projectileForce);
            }

        }

    }


    void Update ()
    {

        //gambiarra
        if (spotPlayer() || playerSpottedBuffer)
            playerSpotted = true;
        else
            playerSpotted = false;
        if (playerSpotted)
        {
            if(Time.time  - shotDelay> 2f)
            {
                shootAtPlayer();
                shotDelay = Time.time;
            }
        }
    }
}
