# ☁️ AWS CloudFormation Templates

Colección de plantillas de AWS CloudFormation para aprovisionar infraestructura en la nube de forma declarativa e incremental. Los templates cubren desde una instancia EC2 básica hasta configuraciones completas con VPC, IAM, S3 y grupos de seguridad.

---

## 📋 Descripción

Este proyecto es un conjunto de plantillas de **Infrastructure as Code (IaC)** escritas en YAML para AWS CloudFormation. El objetivo es aprender y practicar el aprovisionamiento de recursos AWS de manera reproducible, versionada y automatizada, comenzando con ejemplos simples y aumentando gradualmente la complejidad.

---

## 🛠️ Tecnologías

| Tecnología | Descripción |
|---|---|
| **AWS CloudFormation** | Servicio de IaC nativo de AWS |
| **YAML** | Formato de las plantillas |
| **AWS EC2** | Instancias de cómputo |
| **AWS VPC** | Red virtual privada |
| **AWS IAM** | Gestión de identidad y acceso |
| **AWS S3** | Almacenamiento de objetos |
| **AWS EIP** | IP elástica estática |

---

## 📁 Estructura del Proyecto

```
cloudformation/
├── 01-ec2-basic.yaml                          # EC2 básico (nivel inicial)
├── 1.5-public-vpc-subnet-igw-route.yaml       # Red publica base para instancias accesibles
├── 02-ec2-security-group-elastic-ip.yaml      # EC2 con Security Groups e IP elástica
├── 2.5-nat-private-subnet.yaml                # NAT Gateway + subnet privada con salida controlada
├── 03-iam-role-vpc-s3-bucket.yaml             # IAM Role + VPC + S3 Bucket privado
├── 3.5-ec2-ssm-no-ssh.yaml                    # EC2 gestionable por SSM sin abrir SSH publico
├── 04-iam-user-group-vpc-internet-gateway.yaml # IAM User/Group + S3 + VPC + Internet Gateway
├── 4.5-alb-auto-scaling.yaml                  # ALB + Launch Template + Auto Scaling Group
├── 05-iam-admin-group-user-vpc-s3.yaml        # IAM Group de laboratorio + User + S3 + VPC
├── requirements.txt                           # Dependencias para validación local con Python
├── validate_templates.py                      # Validador YAML local compatible con tags de CloudFormation
└── README.md
```

---

## 📄 Detalle de cada Template

### `01-ec2-basic.yaml`
Plantilla mínima. Lanza una instancia EC2 `t2.micro` en `us-east-1a`.
- **Recursos:** `AWS::EC2::Instance`
- **Parámetros:** `SubnetId`
- **Estandarización aplicada:** etiqueta `Name` declarativa para la instancia (`cfn-lab-ec2-basic-<stack>`).
- **Nota:** crea la instancia, pero no configura acceso público, IP pública, Security Group propio ni rutas a Internet.

### `1.5-public-vpc-subnet-igw-route.yaml`
Red pública mínima para desplegar instancias EC2 con salida a Internet.
- **Recursos:** `EC2::VPC`, `EC2::Subnet`, `EC2::InternetGateway`, `EC2::RouteTable`, `EC2::Route`, `EC2::SubnetRouteTableAssociation`
- **Parámetros:** `VpcCidr`, `PublicSubnetCidr`, `AvailabilityZone`
- **Outputs:** `VpcId`, `PublicSubnetId`, `InternetGatewayId`, `RouteTableId`
- **Estandarización aplicada:** etiquetas `Name` declarativas para VPC, subnet pública, IGW y route table.

### `02-ec2-security-group-elastic-ip.yaml`
EC2 con dos Security Groups y una Elastic IP asociada. El `SecurityGroupDescription` se recibe como parámetro.
- **Recursos:** `EC2::Instance`, `EC2::EIP`, `EC2::SecurityGroup` (x2)
- **Parámetros:** `VpcId`, `SubnetId`, `SecurityGroupDescription`, `AdminCidr`
- **Outputs:** IP elástica asignada
- **Estandarización aplicada:** etiquetas `Name` declarativas en EC2, EIP, SG de SSH y SG web.
- **Prerequisito recomendado:** usar primero `1.5-public-vpc-subnet-igw-route.yaml` para obtener una subnet pública funcional.

### `2.5-nat-private-subnet.yaml`
Agrega una subnet privada con salida a Internet a través de NAT Gateway.
- **Recursos:** `EC2::Subnet`, `EC2::EIP`, `EC2::NatGateway`, `EC2::RouteTable`, `EC2::Route`
- **Parámetros:** `VpcId`, `PublicSubnetId`, `PrivateSubnetCidr`, `AvailabilityZone`
- **Outputs:** `PrivateSubnetId`, `NatGatewayId`, `PrivateRouteTableId`

### `03-iam-role-vpc-s3-bucket.yaml`
Crea un rol IAM para EC2 con acceso completo a S3, una VPC y un bucket S3 privado.
- **Recursos:** `IAM::Role`, `EC2::VPC`, `S3::Bucket`
- **Parámetros:** `IamRoleName`, `S3BucketName` (opcionales)
- **Nota:** si no se envían estos parámetros, el template usa nombres físicos declarativos por defecto.

### `3.5-ec2-ssm-no-ssh.yaml`
Despliega una EC2 administrable por Session Manager sin abrir SSH público.
- **Recursos:** `IAM::Role`, `IAM::InstanceProfile`, `EC2::SecurityGroup`, `EC2::Instance`
- **Parámetros:** `VpcId`, `SubnetId`, `LatestAmiId`, `InstanceType`
- **Outputs:** `Ec2InstanceId`, `IamInstanceProfileName`, `IamRoleArn`
- **Estandarización aplicada:** `RoleName` e `InstanceProfileName` declarativos, más etiquetas `Name` para SG y EC2.

### `04-iam-user-group-vpc-internet-gateway.yaml`
Infraestructura completa con usuario y grupo IAM, bucket S3 privado, VPC e Internet Gateway. Incluye Outputs para todos los recursos.
- **Recursos:** `IAM::User`, `IAM::Group`, `S3::Bucket`, `EC2::VPC`, `EC2::InternetGateway`

### `4.5-alb-auto-scaling.yaml`
Despliega una capa web escalable con ALB y Auto Scaling Group.
- **Recursos:** `ELBv2::LoadBalancer`, `ELBv2::TargetGroup`, `ELBv2::Listener`, `EC2::LaunchTemplate`, `AutoScaling::AutoScalingGroup`
- **Parámetros:** `VpcId`, `PublicSubnetA`, `PublicSubnetB`, `LatestAmiId`, `InstanceType`, `DesiredCapacity`, `MinSize`, `MaxSize`
- **Outputs:** `LoadBalancerDnsName`, `AlbTargetGroupArn`

### `05-iam-admin-group-user-vpc-s3.yaml`
Grupo IAM con política mínima de laboratorio, usuario IAM, membresía al grupo, bucket S3 y VPC.
- **Recursos:** `IAM::Group`, `IAM::User`, `IAM::UserToGroupAddition`, `S3::Bucket`, `EC2::VPC`

---

## ✅ Requisitos Previos

- Cuenta de **AWS** activa
- **AWS CLI** instalado y configurado
  ```bash
  aws configure
  ```
- Permisos IAM suficientes para crear los recursos de cada template (EC2, IAM, S3, VPC)
- _(Opcional)_ Acceso a la consola de **AWS CloudFormation**

### Instalación de AWS CLI

```bash
# macOS
brew install awscli

# Verificar instalación
aws --version
```

---

## ⚙️ Configuración

Configura tus credenciales de AWS antes de desplegar:

```bash
aws configure
# AWS Access Key ID:     <tu-access-key>
# AWS Secret Access Key: <tu-secret-key>
# Default region name:   us-east-1
# Default output format: json
```

Para templates con **parámetros** (ej. `02-ec2-security-group-elastic-ip.yaml` o `03-iam-role-vpc-s3-bucket.yaml`), puedes pasarlos en línea o mediante un archivo JSON de parámetros.

### Validar Perfil AWS Activo

Antes de ejecutar comandos de CloudFormation, valida qué perfil/credenciales está usando tu CLI:

```bash
# Ver perfil y origen de credenciales actualmente usados
aws configure list

# Ver el perfil activo por variable de entorno (si aplica)
echo $AWS_PROFILE

# Confirmar identidad real (cuenta/usuario/rol) con el contexto actual
aws sts get-caller-identity

# Probar CloudFormation con un perfil especifico
aws cloudformation list-stacks --profile cristianjonhson

# Fijar perfil para la sesion actual (opcional)
export AWS_PROFILE=cristianjonhson
```

### Convención de Nombres (Estándar del Laboratorio)

| Elemento | Convención | Ejemplo | Nota |
|---|---|---|---|
| Stack name | `cfn-lab-<dominio>-<servicio>-<alcance>` | `cfn-lab-network-public-base` | Se usa en `--stack-name` para crear, esperar y eliminar stacks. |
| Logical ID (CloudFormation) | `PascalCase` por tipo y propósito | `Ec2InstanceSsmManaged`, `RouteTablePublic` | Identificador interno del template; debe ser estable para evitar reemplazos no deseados. |
| Nombre físico explícito | Prefijo `cfn-lab-` + servicio + contexto | `cfn-lab-alb-web`, `cfn-lab-iam-group-admin` | Aplica en propiedades como `Name`, `RoleName`, `InstanceProfileName`, `GroupName`, `UserName`, `BucketName`. |
| Tag Name | `cfn-lab-<recurso>-${AWS::StackName}` | `cfn-lab-ec2-basic-${AWS::StackName}` | Facilita trazabilidad del recurso en consola y costos. |
| Nombre único global (S3) | `cfn-lab-...-${AWS::AccountId}-${AWS::Region}` | `cfn-lab-s3-bucket-ec2-s3-${AWS::AccountId}-${AWS::Region}` | Evita colisiones globales de nombre en buckets S3. |

Reglas rápidas:

1. Mantener siempre el prefijo `cfn-lab-`.
2. Evitar nombres genéricos (`my-user`, `my-group`, `lab-alb`) en recursos físicos.
3. Incluir `${AWS::StackName}` en tags `Name` cuando aplique.
4. Para S3, incluir `${AWS::AccountId}` y `${AWS::Region}` si se define nombre físico.
5. Si un template crea IAM con nombres físicos explícitos, usar `CAPABILITY_NAMED_IAM`.

---

## 🚀 Cómo Desplegar

### Opción 1 — AWS CLI

```bash
# Convencion sugerida para stack names declarativos:
# cfn-lab-<dominio>-<servicio>-<alcance>
# Ejemplos:
# - cfn-lab-network-public-base
# - cfn-lab-ec2-sg-eip
# - cfn-lab-alb-asg-web

# Crear un stack nuevo
aws cloudformation create-stack \
  --stack-name <nombre-del-stack> \
  --template-body file://<nombre-del-archivo>.yaml \
  --capabilities CAPABILITY_NAMED_IAM

# Prerrequisito de red (recomendado): crear VPC + subnet publica con el template 1.5
aws cloudformation create-stack \
  --stack-name cfn-lab-network-public-base \
  --template-body file://1.5-public-vpc-subnet-igw-route.yaml \
  --profile cristianjonhson \
  --no-cli-pager
aws cloudformation wait stack-create-complete \
  --stack-name cfn-lab-network-public-base \
  --profile cristianjonhson

# Obtener VpcId y SubnetId para reutilizarlos en 01, 02 y 3.5
VPC_ID=$(aws cloudformation describe-stacks \
  --stack-name cfn-lab-network-public-base \
  --profile cristianjonhson \
  --query "Stacks[0].Outputs[?OutputKey=='VpcId'].OutputValue" \
  --output text)

SUBNET_ID=$(aws cloudformation describe-stacks \
  --stack-name cfn-lab-network-public-base \
  --profile cristianjonhson \
  --query "Stacks[0].Outputs[?OutputKey=='PublicSubnetId'].OutputValue" \
  --output text)

echo "VPC_ID=$VPC_ID"
echo "SUBNET_ID=$SUBNET_ID"

# Alternativa manual (sin template 1.5): crear solo una subnet dentro de una VPC existente
# Requiere reemplazar vpc-xxxxxxxx por un VPC real.
aws ec2 create-subnet \
  --vpc-id vpc-xxxxxxxx \
  --cidr-block 10.0.10.0/24 \
  --availability-zone us-east-1a \
  --query 'Subnet.SubnetId' \
  --output text \
  --profile cristianjonhson \
  --no-cli-pager

# Ejemplo template 01: EC2 básica
aws cloudformation create-stack \
  --stack-name cfn-lab-ec2-basic \
  --template-body file://01-ec2-basic.yaml \
  --parameters ParameterKey=SubnetId,ParameterValue="$SUBNET_ID" \
  --profile cristianjonhson \
  --no-cli-pager
aws cloudformation wait stack-create-complete --stack-name cfn-lab-ec2-basic --profile cristianjonhson

# Eliminar stack del template 01
aws cloudformation delete-stack --stack-name cfn-lab-ec2-basic
aws cloudformation wait stack-delete-complete --stack-name cfn-lab-ec2-basic

# Esta plantilla solo crea la instancia dentro de la subnet indicada.
# Si necesitas conectarte desde Internet, usa una subnet publica y configura IP publica,
# reglas SSH y salida por Internet en tu red, o usa la plantilla 02.

# Ejemplo template 1.5: crear VPC + subnet publica + Internet Gateway + ruta publica
aws cloudformation create-stack \
  --stack-name cfn-lab-network-public-base \
  --template-body file://1.5-public-vpc-subnet-igw-route.yaml
aws cloudformation wait stack-create-complete --stack-name cfn-lab-network-public-base

# Eliminar stack del template 1.5
aws cloudformation delete-stack --stack-name cfn-lab-network-public-base
aws cloudformation wait stack-delete-complete --stack-name cfn-lab-network-public-base

# Consulta los outputs para obtener VpcId y PublicSubnetId para la plantilla 02
aws cloudformation describe-stacks \
  --stack-name cfn-lab-network-public-base \
  --query 'Stacks[0].Outputs[*].[OutputKey,OutputValue]' \
  --output table

# Ejemplo template 02: EC2 + Security Groups + Elastic IP
aws cloudformation create-stack \
  --stack-name cfn-lab-ec2-sg-eip \
  --template-body file://02-ec2-security-group-elastic-ip.yaml \
  --parameters \
    ParameterKey=VpcId,ParameterValue="vpc-xxxxxxxx" \
    ParameterKey=SubnetId,ParameterValue="subnet-xxxxxxxx" \
    ParameterKey=SecurityGroupDescription,ParameterValue="Mi grupo de seguridad" \
    ParameterKey=AdminCidr,ParameterValue="203.0.113.10/32"

# Reemplaza `vpc-xxxxxxxx` y `subnet-xxxxxxxx` por una VPC y subnet reales de tu cuenta.
# Reemplaza `203.0.113.10/32` por tu IP pública real con máscara /32.

# Esperar a que termine la creación del stack
aws cloudformation wait stack-create-complete \
  --stack-name cfn-lab-ec2-sg-eip

# Obtener directamente la Elastic IP desde los outputs del stack
aws cloudformation describe-stacks \
  --stack-name cfn-lab-ec2-sg-eip \
  --query "Stacks[0].Outputs[?OutputKey=='ElasticIp'].OutputValue" \
  --output text

# Listar todos los recursos creados por el stack
aws cloudformation list-stack-resources \
  --stack-name cfn-lab-ec2-sg-eip

# Eliminar stack del template 02
aws cloudformation delete-stack --stack-name cfn-lab-ec2-sg-eip
aws cloudformation wait stack-delete-complete --stack-name cfn-lab-ec2-sg-eip

# Ejemplo template 03 por defecto (el template aplica nombres declarativos para rol y bucket)
aws cloudformation create-stack \
  --stack-name cfn-lab-iam-vpc-s3-default \
  --template-body file://03-iam-role-vpc-s3-bucket.yaml \
  --capabilities CAPABILITY_NAMED_IAM
aws cloudformation wait stack-create-complete --stack-name cfn-lab-iam-vpc-s3-default

# Eliminar stack del template 03 por defecto
aws cloudformation delete-stack --stack-name cfn-lab-iam-vpc-s3-default
aws cloudformation wait stack-delete-complete --stack-name cfn-lab-iam-vpc-s3-default

# Ejemplo template 03 con nombres personalizados para rol y bucket
aws cloudformation create-stack \
  --stack-name cfn-lab-iam-vpc-s3-custom-names \
  --template-body file://03-iam-role-vpc-s3-bucket.yaml \
  --parameters ParameterKey=IamRoleName,ParameterValue="cfn-lab-iam-role-cris" ParameterKey=S3BucketName,ParameterValue="cfn-lab-s3-bucket-cris-2026" \
  --capabilities CAPABILITY_NAMED_IAM
aws cloudformation wait stack-create-complete --stack-name cfn-lab-iam-vpc-s3-custom-names

# Eliminar stack del template 03 con nombres personalizados
aws cloudformation delete-stack --stack-name cfn-lab-iam-vpc-s3-custom-names
aws cloudformation wait stack-delete-complete --stack-name cfn-lab-iam-vpc-s3-custom-names

# Ejemplo template 2.5: NAT Gateway + subnet privada
aws cloudformation create-stack \
  --stack-name cfn-lab-network-nat-private \
  --template-body file://2.5-nat-private-subnet.yaml \
  --parameters \
    ParameterKey=VpcId,ParameterValue="vpc-xxxxxxxx" \
    ParameterKey=PublicSubnetId,ParameterValue="subnet-xxxxxxxx"
aws cloudformation wait stack-create-complete --stack-name cfn-lab-network-nat-private

# Eliminar stack del template 2.5
aws cloudformation delete-stack --stack-name cfn-lab-network-nat-private
aws cloudformation wait stack-delete-complete --stack-name cfn-lab-network-nat-private

# Ejemplo template 3.5: EC2 administrable por SSM sin SSH
aws cloudformation create-stack \
  --stack-name cfn-lab-ec2-ssm-private \
  --template-body file://3.5-ec2-ssm-no-ssh.yaml \
  --parameters \
    ParameterKey=VpcId,ParameterValue="vpc-xxxxxxxx" \
    ParameterKey=SubnetId,ParameterValue="subnet-xxxxxxxx" \
    ParameterKey=InstanceType,ParameterValue="t2.micro" \
  --capabilities CAPABILITY_NAMED_IAM
aws cloudformation wait stack-create-complete --stack-name cfn-lab-ec2-ssm-private

# Eliminar stack del template 3.5
aws cloudformation delete-stack --stack-name cfn-lab-ec2-ssm-private
aws cloudformation wait stack-delete-complete --stack-name cfn-lab-ec2-ssm-private

# Ejemplo template 04: IAM User + IAM Group + S3 + VPC + Internet Gateway
aws cloudformation create-stack \
  --stack-name cfn-lab-iam-user-group-vpc-igw \
  --template-body file://04-iam-user-group-vpc-internet-gateway.yaml \
  --capabilities CAPABILITY_NAMED_IAM
aws cloudformation wait stack-create-complete --stack-name cfn-lab-iam-user-group-vpc-igw

# Eliminar stack del template 04
aws cloudformation delete-stack --stack-name cfn-lab-iam-user-group-vpc-igw
aws cloudformation wait stack-delete-complete --stack-name cfn-lab-iam-user-group-vpc-igw

# Ejemplo template 4.5: ALB + Auto Scaling
aws cloudformation create-stack \
  --stack-name cfn-lab-alb-asg-web \
  --template-body file://4.5-alb-auto-scaling.yaml \
  --parameters \
    ParameterKey=VpcId,ParameterValue="vpc-xxxxxxxx" \
    ParameterKey=PublicSubnetA,ParameterValue="subnet-aaaaaaa" \
    ParameterKey=PublicSubnetB,ParameterValue="subnet-bbbbbbb"
aws cloudformation wait stack-create-complete --stack-name cfn-lab-alb-asg-web

# Eliminar stack del template 4.5
aws cloudformation delete-stack --stack-name cfn-lab-alb-asg-web
aws cloudformation wait stack-delete-complete --stack-name cfn-lab-alb-asg-web

# Ejemplo template 05: IAM Group con permisos de laboratorio + User + S3 + VPC
aws cloudformation create-stack \
  --stack-name cfn-lab-iam-user-group-vpc-s3 \
  --template-body file://05-iam-admin-group-user-vpc-s3.yaml \
  --capabilities CAPABILITY_NAMED_IAM
aws cloudformation wait stack-create-complete --stack-name cfn-lab-iam-user-group-vpc-s3

# Eliminar stack del template 05
aws cloudformation delete-stack --stack-name cfn-lab-iam-user-group-vpc-s3
aws cloudformation wait stack-delete-complete --stack-name cfn-lab-iam-user-group-vpc-s3

# Eliminar stack del template 1.5 (hacerlo al final para no romper dependencias)
aws cloudformation delete-stack --stack-name cfn-lab-network-public-base
aws cloudformation wait stack-delete-complete --stack-name cfn-lab-network-public-base
```

### Bloque Único: Desplegar y Probar 2.5 → 3.5 → 4.5

Prerrequisito: tener creado el stack `cfn-lab-network-public-base` con `1.5-public-vpc-subnet-igw-route.yaml`.

```bash
# 0) Tomar datos de red del stack 1.5
VPC_ID=$(aws cloudformation describe-stacks --stack-name cfn-lab-network-public-base --query "Stacks[0].Outputs[?OutputKey=='VpcId'].OutputValue" --output text)
PUBLIC_SUBNET_A=$(aws cloudformation describe-stacks --stack-name cfn-lab-network-public-base --query "Stacks[0].Outputs[?OutputKey=='PublicSubnetId'].OutputValue" --output text)
PUBLIC_RT=$(aws cloudformation describe-stacks --stack-name cfn-lab-network-public-base --query "Stacks[0].Outputs[?OutputKey=='RouteTableId'].OutputValue" --output text)

# 1) Crear segunda subnet publica para 4.5 (ALB requiere dos subnets)
PUBLIC_SUBNET_B=$(aws ec2 create-subnet \
  --vpc-id "$VPC_ID" \
  --cidr-block 10.0.3.0/24 \
  --availability-zone us-east-1b \
  --query 'Subnet.SubnetId' \
  --output text)

aws ec2 associate-route-table --route-table-id "$PUBLIC_RT" --subnet-id "$PUBLIC_SUBNET_B"
aws ec2 modify-subnet-attribute --subnet-id "$PUBLIC_SUBNET_B" --map-public-ip-on-launch

# 2) Desplegar 2.5 (NAT + subnet privada)
aws cloudformation create-stack \
  --stack-name cfn-lab-network-nat-private \
  --template-body file://2.5-nat-private-subnet.yaml \
  --parameters \
    ParameterKey=VpcId,ParameterValue="$VPC_ID" \
    ParameterKey=PublicSubnetId,ParameterValue="$PUBLIC_SUBNET_A"
aws cloudformation wait stack-create-complete --stack-name cfn-lab-network-nat-private

# 3) Desplegar 3.5 (EC2 administrable por SSM sin SSH)
PRIVATE_SUBNET_ID=$(aws cloudformation describe-stacks --stack-name cfn-lab-network-nat-private --query "Stacks[0].Outputs[?OutputKey=='PrivateSubnetId'].OutputValue" --output text)

aws cloudformation create-stack \
  --stack-name cfn-lab-ec2-ssm-private \
  --template-body file://3.5-ec2-ssm-no-ssh.yaml \
  --parameters \
    ParameterKey=VpcId,ParameterValue="$VPC_ID" \
    ParameterKey=SubnetId,ParameterValue="$PRIVATE_SUBNET_ID" \
    ParameterKey=InstanceType,ParameterValue="t2.micro" \
  --capabilities CAPABILITY_NAMED_IAM
aws cloudformation wait stack-create-complete --stack-name cfn-lab-ec2-ssm-private

# Prueba 3.5: validar que la instancia aparece en SSM
INSTANCE_ID=$(aws cloudformation describe-stacks --stack-name cfn-lab-ec2-ssm-private --query "Stacks[0].Outputs[?OutputKey=='Ec2InstanceId'].OutputValue" --output text)
aws ssm describe-instance-information --filters "Key=InstanceIds,Values=$INSTANCE_ID" --query 'InstanceInformationList[0].PingStatus' --output text

# 4) Desplegar 4.5 (ALB + Auto Scaling)
aws cloudformation create-stack \
  --stack-name cfn-lab-alb-asg-web \
  --template-body file://4.5-alb-auto-scaling.yaml \
  --parameters \
    ParameterKey=VpcId,ParameterValue="$VPC_ID" \
    ParameterKey=PublicSubnetA,ParameterValue="$PUBLIC_SUBNET_A" \
    ParameterKey=PublicSubnetB,ParameterValue="$PUBLIC_SUBNET_B"
aws cloudformation wait stack-create-complete --stack-name cfn-lab-alb-asg-web

# Prueba 4.5: obtener DNS del ALB y probar respuesta HTTP
ALB_DNS=$(aws cloudformation describe-stacks --stack-name cfn-lab-alb-asg-web --query "Stacks[0].Outputs[?OutputKey=='LoadBalancerDnsName'].OutputValue" --output text)
curl "http://$ALB_DNS"
```

### Opción 2 — Consola de AWS

1. Ir a **AWS Console → CloudFormation → Create Stack**
2. Seleccionar **"Upload a template file"**
3. Subir el archivo `.yaml` deseado
4. Completar los parámetros requeridos y seguir el asistente

### Actualizar un Stack Existente

```bash
aws cloudformation update-stack \
  --stack-name <nombre-del-stack> \
  --template-body file://<nombre-del-archivo>.yaml \
  --capabilities CAPABILITY_NAMED_IAM
```

### Eliminar un Stack

```bash
aws cloudformation delete-stack --stack-name <nombre-del-stack>
```

### Alternativa Manual Para Red Pública

Si no quieres usar `1.5-public-vpc-subnet-igw-route.yaml`, puedes preparar la red manualmente con AWS CLI creando Internet Gateway, route table, asociación de subnet y habilitando IP pública en la subnet.

---

## 🔍 Validar un Template

Antes de desplegar, se recomienda validar la sintaxis del template:

```bash
aws cloudformation validate-template \
  --template-body file://<nombre-del-archivo>.yaml
```

### Validación Local con Python

Si quieres una validación rápida sin llamar a AWS, puedes parsear localmente los templates con Python. Este validador entiende tags de CloudFormation como `!Ref`, `!Sub`, `!If` y similares.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Validar todos los templates del repositorio
python validate_templates.py

# Validar un template concreto
python validate_templates.py 03-iam-role-vpc-s3-bucket.yaml
```

Esta validación local comprueba sintaxis YAML y compatibilidad con las etiquetas intrínsecas de CloudFormation, pero no sustituye la validación semántica de AWS.

---

## ⚠️ Consideraciones Importantes

- El template `02-ec2-security-group-elastic-ip.yaml` ahora restringe SSH por parámetro `AdminCidr`; usa tu IP pública con máscara `/32`.
- El template `01-ec2-basic.yaml` requiere `SubnetId` si tu cuenta no tiene VPC por defecto.
- El template `02-ec2-security-group-elastic-ip.yaml` requiere `VpcId` y `SubnetId`; el flujo recomendado es crear primero la red con `1.5-public-vpc-subnet-igw-route.yaml`.
- El flag `--capabilities CAPABILITY_NAMED_IAM` es obligatorio en los templates que crean recursos IAM cuando existen nombres físicos explícitos (por ejemplo, en `03-iam-role-vpc-s3-bucket.yaml` y `3.5-ec2-ssm-no-ssh.yaml`).
- El template `01-ec2-basic.yaml` usa una AMI de Amazon Linux obtenida desde SSM Parameter Store para evitar IDs obsoletos.
- `S3BucketName` en S3 es opcional; si lo defines, debe ser globalmente único en AWS.
- `03-iam-role-vpc-s3-bucket.yaml` usa un bucket privado; si necesitas exponer objetos públicamente, añade una política específica en lugar de abrir el bucket completo.
- `05-iam-admin-group-user-vpc-s3.yaml` ya no asigna `AdministratorAccess`; usa permisos mínimos de laboratorio para reducir riesgo.

---

## 📌 Orden de Aprendizaje Sugerido

```
01-ec2-basic.yaml
       ↓
1.5-public-vpc-subnet-igw-route.yaml
       ↓
02-ec2-security-group-elastic-ip.yaml
       ↓
2.5-nat-private-subnet.yaml
       ↓
3.5-ec2-ssm-no-ssh.yaml
       ↓
4.5-alb-auto-scaling.yaml
       ↓
04-iam-user-group-vpc-internet-gateway.yaml
       ↓
05-iam-admin-group-user-vpc-s3.yaml
       ↓
03-iam-role-vpc-s3-bucket.yaml
```

---

## 📚 Referencias

- [Documentación oficial de AWS CloudFormation](https://docs.aws.amazon.com/cloudformation/)
- [Referencia de tipos de recursos](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html)
- [AWS CLI — CloudFormation](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/)
- [Buenas prácticas de CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html)

---

## 👤 Autor

**crisjonhson** — [@crisjonhson](https://github.com/crisjonhson)
