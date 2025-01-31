/*******************************************************************************
 *
 *  Filename    : bprimeKit_vertex.cc
 *  Description : vertex info filling 
 *  Author      : Yi-Mu "Enoch" Chen [ ensc@hep1.phys.ntu.edu.tw ]
 *
*******************************************************************************/
#include "MyAna/bprimeKit/interface/bprimeKit.h"


//------------------------------------------------------------------------------ 
//   bprimeKit method implementation 
//------------------------------------------------------------------------------ 
bool bprimeKit::fillVertex( const edm::Event& iEvent , const edm::EventSetup& iSetup )
{
   bool   gotPrimVtx;
   double PVBS_Pt_Max;
      
   if( debug_ > 5 ) { cout << "Fill Vertex Info.\n"; }
   memset( &VertexInfo, 0x00, sizeof( VertexInfo ) );
   
   //----- Vertices without beamspot constraints  -----------------------------------------------------
   Signal_Vz = 0.;
   gotPrimVtx = false;
   if( VertexHandle.isValid() && !VertexHandle.failedToGet() && VertexHandle->size() > 0 ) {
      const VertexList Vertices = *VertexHandle;
      PrimVtx = *( Vertices.begin() ); //Uly 2012-07-19: just get something valid to start with
      for( VertexListCIT it_vtx = Vertices.begin();it_vtx != Vertices.end(); it_vtx++ ) {
         if ( VertexInfo.Size >= MAX_Vertices ) {
            cout << "PV " << VertexInfo.Size << endl;
            cerr << "ERROR: number of  Tracks exceeds the size of array." << endl;
            break;
         }
         VertexInfo.Type           [ VertexInfo.Size ] = 0                        ; //Vertices WITHOUT the Beam Spot constraint
         VertexInfo.isValid        [ VertexInfo.Size ] = it_vtx->isValid()        ;
         VertexInfo.isFake         [ VertexInfo.Size ] = it_vtx->isFake()         ; //Uly 2011-05-16
         VertexInfo.Ndof           [ VertexInfo.Size ] = it_vtx->ndof()           ;
         VertexInfo.NormalizedChi2 [ VertexInfo.Size ] = it_vtx->normalizedChi2() ;
         VertexInfo.x              [ VertexInfo.Size ] = it_vtx->x()              ;
         VertexInfo.y              [ VertexInfo.Size ] = it_vtx->y()              ;
         VertexInfo.z              [ VertexInfo.Size ] = it_vtx->z()              ;
         VertexInfo.Rho            [ VertexInfo.Size ] = it_vtx->position().Rho() ;
         VertexInfo.Pt_Sum         [ VertexInfo.Size ] = 0.                       ;
         VertexInfo.Pt_Sum2        [ VertexInfo.Size ] = 0.                       ;

         for ( auto it = it_vtx->tracks_begin(); it != it_vtx->tracks_end(); it++ ) {
            VertexInfo.Pt_Sum  [ VertexInfo.Size ] += ( *it )->pt();
            VertexInfo.Pt_Sum2 [ VertexInfo.Size ] += ( ( *it )->pt() * ( *it )->pt() );
         }
         if( !gotPrimVtx && ( !it_vtx->isFake() && it_vtx->ndof() >= 4. && it_vtx->z() <= 24. && it_vtx->position().Rho() <= 2. ) ) {
            PrimVtx = *it_vtx;
            gotPrimVtx = true;
         }
         VertexInfo.Size++;
      }
      Signal_Vz = PrimVtx.z();
   }

   //----- Vertices with beamspot constraint  ---------------------------------------------------------
   PVBS_Pt_Max = -100. ; 
   if( VertexHandleBS.isValid() && !VertexHandleBS.failedToGet() && VertexHandleBS->size() > 0 ) {
      const VertexList VerticesBS = *VertexHandleBS;
      for( VertexListCIT it_vtx = VerticesBS.begin();it_vtx != VerticesBS.end(); it_vtx++ ) {
         if ( VertexInfo.Size >= MAX_Vertices ) {
            cout << "PVBS " << VertexInfo.Size << endl;
            cerr << "ERROR: number of  Vertices exceeds the size of array." << endl;
            break;//exit(0);
         }
         VertexInfo.Type           [ VertexInfo.Size ] = 1                        ; //Vertices WITH the Beam Spot constraint
         VertexInfo.isValid        [ VertexInfo.Size ] = it_vtx->isValid()        ;
         VertexInfo.isFake         [ VertexInfo.Size ] = it_vtx->isFake()         ; //Uly 2011-05-16
         VertexInfo.Ndof           [ VertexInfo.Size ] = it_vtx->ndof()           ;
         VertexInfo.NormalizedChi2 [ VertexInfo.Size ] = it_vtx->normalizedChi2() ;
         VertexInfo.x              [ VertexInfo.Size ] = it_vtx->x()              ;
         VertexInfo.y              [ VertexInfo.Size ] = it_vtx->y()              ;
         VertexInfo.z              [ VertexInfo.Size ] = it_vtx->z()              ;
         VertexInfo.Rho            [ VertexInfo.Size ] = it_vtx->position().Rho() ;
         VertexInfo.Pt_Sum         [ VertexInfo.Size ] = 0.                       ;
         VertexInfo.Pt_Sum2        [ VertexInfo.Size ] = 0.                       ;

         for ( auto it = it_vtx->tracks_begin(); it != it_vtx->tracks_end(); it++ ) {
            VertexInfo.Pt_Sum  [ VertexInfo.Size ] += ( *it )->pt();
            VertexInfo.Pt_Sum2 [ VertexInfo.Size ] += ( ( *it )->pt() * ( *it )->pt() );
         }
         if( VertexInfo.Pt_Sum[VertexInfo.Size] >= PVBS_Pt_Max ) {
            PVBS_Pt_Max = VertexInfo.Pt_Sum[VertexInfo.Size];
            PrimVtx_BS = *it_vtx;
         }
         VertexInfo.Size++;
      }
   }
   return true;
}
